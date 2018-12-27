import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';

const styles = () => ({
  root: {
    padding: '32px 64px',
    backgroundColor: '#ffffff',
  },
});

const Footer = (props) => {
  const { classes } = props;
  return (
    <div className={classes.root}>
      <Grid container>
        <Grid item xs={12} sm={6}>
          <Typography component="h5">Features</Typography>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Typography component="h5">About</Typography>
        </Grid>
      </Grid>
    </div>
  );
};
Footer.propTypes = {
  classes: PropTypes.shape().isRequired,
};
export default withStyles(styles)(Footer);
