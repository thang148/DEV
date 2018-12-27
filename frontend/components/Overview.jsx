/* eslint-disable react/destructuring-assignment,max-len,react/no-danger,linebreak-style */
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import ListItemText from '@material-ui/core/ListItemText';
import Grid from '@material-ui/core/Grid/Grid';
import Typography from '@material-ui/core/Typography/Typography';

import __ from '../lang/vi';

const styles = (theme) => ({
  grid: {
    borderWidth: '1px',
    borderStyle: 'solid',
    borderColor: '#00000045',
    backgroundColor: theme.palette.background.paper,
  },
  tabContainer: {
    width: 'calc( 100% - 250px )',
    padding: '10px 10px 10px 20px',
    backgroundColor: '#eee',
    minHeight: '500px',
  },
  list: {
    width: '100%',
    maxWidth: 250,
    backgroundColor: theme.palette.background.paper,
  },
});
const TabContainer = (props) => (
  <Typography className={props.className} component="div">
    {props.children}
  </Typography>
);
TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
};
TabContainer.defaultProps = {
  className: '',
};

class Overview extends Component {
  state = {
    selectedIndex: 0,
  };

  handleListItemClick = (event, index) => {
    this.setState({ selectedIndex: index });
  };

  render() {
    const { classes } = this.props;
    const { contest } = this.props;
    const { selectedIndex } = this.state;
    if (!contest) return <div>Loading</div>;
    return (
      <Grid
        container
        direction="row"
        justify="flex-end"
        alignItems="stretch"
        className={classes.grid}
      >
        {selectedIndex === 0 && (
          <TabContainer className={classes.tabContainer}>
            <div
              dangerouslySetInnerHTML={{ __html: contest.fullDescription }}
            />
          </TabContainer>
        )}
        {selectedIndex === 1 && (
          <TabContainer className={classes.tabContainer}>
            <div dangerouslySetInnerHTML={{ __html: contest.evaluation }} />
          </TabContainer>
        )}
        {selectedIndex === 2 && (
          <TabContainer className={classes.tabContainer}>
            <div dangerouslySetInnerHTML={{ __html: contest.prizes }} />
          </TabContainer>
        )}
        {selectedIndex === 3 && (
          <TabContainer className={classes.tabContainer}>
            <div dangerouslySetInnerHTML={{ __html: contest.timeline }} />
          </TabContainer>
        )}
        <div className={classes.list}>
          <List component="nav" disablePadding>
            <ListItem
              button
              selected={selectedIndex === 0}
              onClick={(event) => this.handleListItemClick(event, 0)}
            >
              <ListItemText primary={__.common.Description} />
            </ListItem>
            <ListItem
              button
              selected={selectedIndex === 1}
              onClick={(event) => this.handleListItemClick(event, 1)}
            >
              <ListItemText primary={__.common.Evaluation} />
            </ListItem>
            <ListItem
              button
              selected={selectedIndex === 2}
              onClick={(event) => this.handleListItemClick(event, 2)}
            >
              <ListItemText primary={__.common.Prize} />
            </ListItem>
            <ListItem
              button
              selected={selectedIndex === 3}
              onClick={(event) => this.handleListItemClick(event, 3)}
            >
              <ListItemText primary={__.common.Timeline} />
            </ListItem>
          </List>
        </div>
      </Grid>
    );
  }
}

Overview.propTypes = {
  classes: PropTypes.shape(),
  contest: PropTypes.shape(),
};
Overview.defaultProps = {
  classes: () => {},
  contest: () => {},
};

export default withStyles(styles)(Overview);
