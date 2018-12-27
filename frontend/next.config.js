const withSourceMaps = require('@zeit/next-source-maps');
const withCSS = require('@zeit/next-css');

module.exports = {
  ...withCSS(
    withSourceMaps({
      webpack(config) {
        return config;
      },
    }),
  ),
  publicRuntimeConfig: {
    host: process.env.HOST || 'http://localhost:3000',
  },
};
