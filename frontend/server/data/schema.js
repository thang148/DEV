const { makeExecutableSchema } = require('graphql-tools');
const fs = require('fs');
const path = require('path');
// const debug = require('debug')('aivivn:schema');
const resolvers = require('./resolvers');

const typeDefs = fs.readFileSync(path.join(__dirname, './schema.gql'), 'utf-8');

module.exports = makeExecutableSchema({
  typeDefs,
  resolvers,
});
