import { HttpLink } from 'apollo-link-http';
import { withData } from 'next-apollo';
import getConfig from 'next/config';

const { publicRuntimeConfig } = getConfig();

const config = (ctx) => ({
  link: new HttpLink({
    uri: `${publicRuntimeConfig.host}/graphql`, // Server URL (must be absolute)
    headers: {
      Authorization: ctx && ctx.req.cookies.token,
    },
    opts: {
      credentials: 'same-origin', // Additional fetch() options like `credentials` or `headers`
    },
  }),
});

export default withData(config);
