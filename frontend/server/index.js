const bodyParser = require('body-parser');
const cors = require('cors');
const express = require('express');
const cookieParser = require('cookie-parser');
const { graphqlExpress, graphiqlExpress } = require('apollo-server-express');
const next = require('next');

const routes = require('../common/routes');

require('dotenv').config();

const schema = require('./data/schema');

const port = process.env.PORT || 3000;

const dev = process.env.NODE_ENV !== 'production';

const app = next({
  dev,
});

const handle = routes.getRequestHandler(app);

app.prepare().then(() => {
  const server = express();
  server.use(cookieParser());
  server.use(
    cors({
      origin: ['localhost:3000', /.*amazonaws\.com/],
    }),
  );
  server.use(
    '/graphql',
    bodyParser.json(),
    graphqlExpress((req, res) => {
      const context = {
        login: (accessToken) => {
          res.cookie('token', accessToken);
        },
        accessToken: req.cookies.token || req.headers.authorization,
      };

      return {
        schema,
        context,
      };
    }),
  );

  server.use(
    '/graphiql',
    graphiqlExpress({
      endpointURL: '/graphql',
    }),
  );

  server.get('*', (req, res) => handle(req, res));

  // Start express server
  server.listen(
    port,
    () => console.log('> GraphQL Server Listening on Port', port), // eslint-disable-line
  );
});
