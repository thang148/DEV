const routes = require('next-routes');

module.exports = routes()
  .add('contests', '/', 'index')
  .add('contest', '/contests/:id')
  .add('user', '/users/:username', 'user');
