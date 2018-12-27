/* eslint-disable react/forbid-prop-types */
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Tooltip from '@material-ui/core/Tooltip';
import PropTypes from 'prop-types';
import React from 'react';

import { Link } from '../common/routes';

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
  change: {
    width: '50px',
    '& > span': {
      display: 'flex',
      alignSelf: 'baseline',
    },
    '& > span.header.change__up': {
      color: 'rgba(0, 0, 0, 0.54)',
    },
    '& > span.header.change__up> span.fa': {
      fontSize: '1.5em',
      marginTop: '0.3em',
    },
    '& > span> span.fa': {
      fontSize: '1em',
      marginRight: '3px',
    },
    '& > span.change__up> span.fa': {
      marginTop: '0.6em',
    },
    '& > span.change__up': {
      color: 'green',
    },
    '& > span.change__down': {
      color: 'red',
    },
  },
});

function renderTeamMember(members) {
  return members.map((member) => (
    <Tooltip title={member.username} key={member.id}>
      <span>
        <Link route="user" params={{ username: member.username }}>
          <a>
            <img
              className="avatar_thumb"
              src={member.user.avatar}
              alt="avatar"
            />
          </a>
        </Link>
      </span>
    </Tooltip>
  ));
}
function renderChangeRange(value) {
  if (value > 0) {
    return (
      <span className="change__up">
        <span className="fa fa-2x fa-sort-up" />
        <span>{value}</span>
      </span>
    );
  }
  if (value < 0) {
    return (
      <span className="change__down">
        <span className="fa fa-2x fa-sort-down" />
        <span>{Math.abs(value)}</span>
      </span>
    );
  }
  return <span>-</span>;
}
function SimpleTable(props) {
  const { classes, teams } = props;
  const { items } = teams;

  return (
    <Paper className={classes.root}>
      <Table className={classes.table}>
        <TableHead>
          <TableRow>
            <TableCell>#</TableCell>
            <TableCell className={classes.change}>
              <span className="header change__up">
                <span className="fa fa-2x fa-sort-up" />
                <span>1w</span>
              </span>
            </TableCell>
            <TableCell>Team Name</TableCell>
            <TableCell numeric padding="none">
              Team Members
            </TableCell>
            <TableCell>Score</TableCell>
            <TableCell>Entries</TableCell>
            <TableCell>Last Submission</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {items &&
            items.map((team, index) => (
              <TableRow key={team.id}>
                <TableCell scope="row">{index + 1}</TableCell>
                <TableCell scope="row" className={classes.change}>
                  {renderChangeRange(team.change)}
                </TableCell>
                <TableCell scope="row">{team.name}</TableCell>
                <TableCell
                  scope="row"
                  numeric
                  padding="none"
                  className={classes.team}
                >
                  <span>{renderTeamMember(team.members)}</span>
                </TableCell>
                <TableCell scope="row">{team.publicScore}</TableCell>
                <TableCell scope="row">{team.numSubmissions}</TableCell>
                <TableCell scope="row">
                  {team.lastSubmissionAt
                    ? moment(team.lastSubmissionAt).fromNow()
                    : '-'}
                </TableCell>
              </TableRow>
            ))}
        </TableBody>
      </Table>
      <style>
        {`
          .change { display: flex; }
          .change > span { align-self: flex-end; }
          .change > span.fa { height: 17px; }
        `}
      </style>
    </Paper>
  );
}

SimpleTable.propTypes = {
  classes: PropTypes.object.isRequired,
  teams: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleTable);
