import Head from 'next/head';
import PropTypes from 'prop-types';
import React from 'react';
import { withStyles } from '@material-ui/core';

import Footer from './Footer';
import Nav from './Nav';

const styles = () => ({
  root: {},
  content: {
    margin: '64px auto',
    width: '1200px',
  },
});
const Layout = ({ title, children, classes }) => (
  <div className={classes.root}>
    <Head>
      <title>{title}</title>
    </Head>
    <Nav />
    <div className={classes.content}>{children}</div>
    <Footer />
  </div>
);

Layout.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  classes: PropTypes.shape().isRequired,
};
export default withStyles(styles)(Layout);
