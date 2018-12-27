import React from 'react';
import PropTypes from 'prop-types';
import gql from 'graphql-tag';
import { Mutation } from 'react-apollo';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
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

const LOGIN = gql`
  mutation Login($email: String!, $password: String!) {
    login(email: $email, password: $password) {
      user {
        email
      }
      error {
        message
      }
    }
  }
`;

class SignIn extends React.Component {
  state = {
    email: 'testuser',
    password: 'testpassword',
  };

  handleInputChange = (event) => {
    const { target } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const { name } = target;

    this.setState({
      [name]: value,
    });
  };

  handleFormSubmit = async (e, login, client) => {
    e.preventDefault();
    const { password, email } = this.state;
    const { data: { login: { error } } } = await login({ variables: { password, email } });
    if (!error) {
      client.resetStore();
      window.location.href = '/';
      /* TODO: Change to Router.replace('/');
       * https://github.com/apollographql/react-apollo/issues/807
       * */
    }
  };

  render() {
    const { classes } = this.props;
    const { email, password } = this.state;
    return (
      <Mutation mutation={LOGIN}>
        {(login, { data, client }) => (
          <Layout title="Index">
            <CssBaseline />
            <main className={classes.layout}>
              <Paper className={classes.paper}>
                <Avatar className={classes.avatar}>
                  <LockIcon />
                </Avatar>
                <Typography variant="headline">{__.common.SignIn}</Typography>
                <form
                  className={classes.form}
                  onSubmit={(e) => this.handleFormSubmit(e, login, client)}
                >
                  <FormControl margin="normal" required fullWidth>
                    <InputLabel htmlFor="email">{__.common.Username}</InputLabel>
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
                  <FormControlLabel
                    control={<Checkbox value="remember" color="primary" />}
                    label="Remember me"
                  />
                  <Button
                    type="submit"
                    fullWidth
                    variant="raised"
                    color="primary"
                    className={classes.submit}
                  >
                    {__.common.SignIn}
                  </Button>
                </form>
                {data && data.login.error ? (
                  <Typography color="error">
                    {data.login.error.message}
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

SignIn.propTypes = {
  classes: PropTypes.shape().isRequired,
};

export default withData(withStyles(styles)(SignIn));
