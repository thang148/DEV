/* eslint-disable react/prop-types */
import React from 'react';
import Button from '@material-ui/core/Button/Button';
import { withStyles } from '@material-ui/core/styles';
import { withRouter } from 'next/router';

const styles = {
  active: {
    backgroundColor: '#fff',
    color: '#000',
    '&:hover': {
      backgroundColor: '#fff',
      color: '#000',
    },
  },
};

const NavLink = ({
  children, router, href, className, classes,
}) => {
  const isActive = router.pathname === href ? classes.active : '';
  const classList = className ? className + isActive : isActive;
  const handleClick = (e) => {
    e.preventDefault();
    router.push(href);
  };

  return (
    <Button
      href={href}
      onClick={handleClick}
      color="inherit"
      className={classList}
    >
      {children}
    </Button>
  );
};

export default withRouter(withStyles(styles)(NavLink));
