/* eslint-disable react/forbid-prop-types */
import Router from 'next/router';
import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Avatar from '@material-ui/core/Avatar';

import gql from 'graphql-tag';
import { Query } from 'react-apollo';

import Button from '@material-ui/core/Button';
import withData from '../gql-lib/apollo';
import { Link } from '../common/routes';
import __ from '../lang/vi';
import { removeCookie } from '../lib/session';
import NavLink from './NavLink';

const styles = (theme) => ({
  row: {
    display: 'flex',
    justifyContent: 'center',
  },
  avatar: {
    margin: theme.spacing.unit,
  },
});
const ME_QUERY = gql`
  query me {
    me {
      username
      avatar
    }
  }
`;
const logout = (client) => {
  removeCookie('token');
  client.resetStore();
  Router.replace('/');
};
const NavBar = ({ classes }) => (
  <AppBar position="fixed">
    <Toolbar>
      <Link href="/">
        <Typography variant="title" color="inherit" style={{ flexGrow: 1 }}>
            AIviVN
        </Typography>
      </Link>
      <NavLink href="/rankings">{__.common.Ranking}</NavLink>
      <Query query={ME_QUERY}>
        { ({ client, data: { me } }) => {
          if (me) {
            return (
              <React.Fragment>
                <Link route="user" params={{ username: me.username }}>
                  <a>
                    <Avatar
                      alt={`${me.username}'s Avatar`}
                      src={me.avatar}
                      className={classes.avatar}
                    />
                  </a>
                </Link>
                <Button onClick={() => logout(client)}>{__.common.Logout}</Button>
              </React.Fragment>
            );
          }
          return (
            <React.Fragment>
              <NavLink href="/signin">{__.common.SignIn}</NavLink>
              <NavLink href="/signup">{__.common.SignUp}</NavLink>
            </React.Fragment>
          );
        }
      }
      </Query>
    </Toolbar>
  </AppBar>
);

NavBar.propTypes = {
  classes: PropTypes.object.isRequired,
};
export default withStyles(styles)(NavBar);
