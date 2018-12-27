/* eslint-disable react/forbid-prop-types */
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import PropTypes from 'prop-types';
import React from 'react';

const moment = require('moment');

const styles = (theme) => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
  team: {
    minWidth: '135px',
    '& .avatar_thumb': {
      width: '25px',
      height: '25px',
      borderRadius: '3px',
      marginRight: '2px',
      display: 'inline-block',
    },
  },
});

function SimpleTable(props) {
  const { classes, data } = props;
  const items = data;

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell>Contest</TableCell>
            <TableCell>Team Name</TableCell>
            <TableCell>Rank</TableCell>
            <TableCell>On Going</TableCell>
            <TableCell />
          </TableRow>
        </TableHead>
        <TableBody>
          {items.map((item, index) => (
            <TableRow key={item.id}>
              <TableCell scope="row">{index + 1}</TableCell>
              <TableCell scope="row">{item.contestName}</TableCell>
              <TableCell scope="row">{item.publicScore}</TableCell>
              <TableCell scope="row">{item.entries}</TableCell>
              <TableCell scope="row">{moment(item.last).fromNow()}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}

SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
  data: PropTypes.array.isRequired,
};

export default withStyles(styles)(SimpleTable);
