/* eslint-disable react/destructuring-assignment, eslint-disable react/jsx-boolean-value */
import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper/Paper';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import withData from '../gql-lib/apollo';
import Layout from '../components/Layout';
import __ from '../lang/vi';

const moment = require('moment');

moment.locale('vi');
const POSTS_PER_PAGE = 10;
const generateMedals = (medals) => {
  const [gold, silver, bronze] = medals;
  return (
    <React.Fragment>
      <span className="medal medal--gold">
        <i className="fa fa-medal medal__icon" />
        {gold}
      </span>
      <span className="medal medal--silver">
        <i className="fa fa-medal medal__icon" />
        {silver}
      </span>
      <span className="medal medal--bronze">
        <i className="fa fa-medal medal__icon" />
        {bronze}
      </span>
    </React.Fragment>
  );
};

const Ranking = (props) => {
  const { users } = props.data;
  return (
    <Layout title={__.common.Ranking}>
      <Paper className="root">
        <Table className="table">
          <TableHead>
            <TableRow>
              <TableCell numeric padding="none">
                Rank
              </TableCell>
              <TableCell>User</TableCell>
              <TableCell numeric>Medals</TableCell>
              <TableCell numeric>Best Contest Rank</TableCell>
              <TableCell numeric>Contests</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users &&
              users.map((user) => (
                <Link key={user.id} href={`/users/${user.username}`}>
                  <TableRow hover className="row--hover">
                    <TableCell scope="row" numeric>
                      {user.rank}
                    </TableCell>
                    <TableCell scope="row">
                      <img
                        className="avatar_thumb"
                        src={user.avatar}
                        alt="avatar"
                      />
                      <span>{user.fullName}</span>
                      <span style={{ float: 'right' }}>
                        {moment(user.createdAt).fromNow()}
                      </span>
                    </TableCell>
                    <TableCell scope="row" numeric>
                      {user.medals && generateMedals(user.medals)}
                    </TableCell>
                    <TableCell scope="row" numeric>
                      {user.bestContestRank}
                    </TableCell>
                    <TableCell scope="row" numeric>
                      {user.contests}
                    </TableCell>
                  </TableRow>
                </Link>
              ))}
          </TableBody>
        </Table>
        <style>
          {`
            .root { width: 100%; overflow-x: auto; }
            .table { min-width: 700}
            .row--hover:hover { cursor: pointer }
            .avatar_thumb {
              width: 25px;
              height: 25px;
              border-radius: 3px;
              margin-right: 10px;
              display: inline-block;
            }
            .medal { margin-right: 10px; width: 40px; display: inline-block; text-align: left;}
            .medal .medal__icon { margin-right: 3px;  }
            .medal--gold .medal__icon { color: #FDC824 }
            .medal--silver .medal__icon { color: #E0DFE5 }
            .medal--bronze .medal__icon { color: #EE9048 }
          `}
        </style>
      </Paper>
    </Layout>
  );
};
Ranking.propTypes = {
  data: PropTypes.shape(),
};
Ranking.defaultProps = {
  data: () => {},
};

const users = gql`
  query users($skip: Int!, $take: Int!) {
    users(skip: $skip, take: $take) {
      id
      fullName
      username
      avatar
      contests
      medals
      rank
      bestContestRank
      createdAt
    }
  }
`;

export default withData(
  graphql(users, {
    options: {
      variables: {
        skip: 0,
        take: POSTS_PER_PAGE,
      },
    },
    props: ({ data }) => ({
      data,
      loadMore: () => data.fetchMore({
        variables: {
          skip: data.members.length,
        },
        updateQuery: (previousResult, { fetchMoreResult }) => {
          if (!fetchMoreResult) {
            return previousResult;
          }
          return Object.assign({}, previousResult, {
            // Append the new posts results to the old one
            users: [...previousResult.users, ...fetchMoreResult.users],
          });
        },
      }),
    }),
  })(Ranking),
);
