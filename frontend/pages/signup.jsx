import Router from 'next/router';
import gql from 'graphql-tag';
import PropTypes from 'prop-types';
import React from 'react';
import { Mutation } from 'react-apollo';

import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import Paper from '@material-ui/core/Paper';
import withStyles from '@material-ui/core/styles/withStyles';
import Typography from '@material-ui/core/Typography';
import LockIcon from '@material-ui/icons/LockOutlined';

import withData from '../gql-lib/apollo';
import Layout from '../components/Layout';
import __ from '../lang/vi';

const styles = (theme) => ({
  layout: {
    width: 'auto',
    display: 'block', // Fix IE11 issue.
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: theme.spacing.unit * 10,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme
      .spacing.unit * 3}px`,
  },
  avatar: {
    margin: theme.spacing.unit,
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE11 issue.
    marginTop: theme.spacing.unit,
  },
  submit: {
    marginTop: theme.spacing.unit * 3,
  },
});

const REGISTER = gql`
  mutation Register($username: String!, $email: String!, $password: String!) {
    register(username: $username, email: $email, password: $password) {
      user {
        id
      }
      error {
        message
      }
    }
  }
`;

class SignUp extends React.Component {
  state = {
    username: '',
    email: '',
    password: '',
  };

  handleInputChange = (event) => {
    const { target } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const { name } = target;

    this.setState({
      [name]: value,
    });
  };

  handleFormSubmit = async (e, register) => {
    e.preventDefault();
    const { username, email, password } = this.state;
    const { data } = await register({ variables: { username, email, password } });
    if (!data.register.error) {
      Router.replace('/signin');
    }
  };

  render() {
    const { classes } = this.props;
    const { username, email, password } = this.state;
    return (
      <Mutation mutation={REGISTER}>
        {(register, { data }) => (
          <Layout title={__.common.SignUp}>
            <CssBaseline />
            <main className={classes.layout}>
              <Paper className={classes.paper}>
                <Avatar className={classes.avatar}>
                  <LockIcon />
                </Avatar>
                <Typography variant="headline">{__.common.SignUp}</Typography>
                <form
                  className={classes.form}
                  onSubmit={(e) => this.handleFormSubmit(e, register)}
                >
                  <FormControl margin="normal" required fullWidth>
                    <InputLabel htmlFor="username">{__.common.Username}</InputLabel>
                    <Input
                      id="username"
                      name="username"
                      autoFocus
                      value={username}
                      onChange={this.handleInputChange}
                    />
                  </FormControl>
                  <FormControl margin="normal" required fullWidth>
                    <InputLabel htmlFor="email">{__.common.EmailAddress}</InputLabel>
                    <Input
                      id="email"
                      name="email"
                      autoFocus
                      value={email}
                      onChange={this.handleInputChange}
                    />
                  </FormControl>
                  <FormControl margin="normal" required fullWidth>
                    <InputLabel htmlFor="password">{__.common.Password}</InputLabel>
                    <Input
                      name="password"
                      type="password"
                      id="password"
                      value={password}
                      onChange={this.handleInputChange}
                    />
                  </FormControl>
                  <Button
                    type="submit"
                    fullWidth
                    variant="raised"
                    color="primary"
                    className={classes.submit}
                  >
                    {__.common.SignUp}
                  </Button>
                </form>
                {data && data.register.error ? (
                  <Typography color="error">
                    {data.register.error.message}
                  </Typography>
                ) : null}
              </Paper>
            </main>
          </Layout>
        )}
      </Mutation>
    );
  }
}

SignUp.propTypes = {
  classes: PropTypes.object.isRequired, // eslint-disable-line
};

export default withData(withStyles(styles)(SignUp));
