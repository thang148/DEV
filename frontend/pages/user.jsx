/* eslint-disable react/destructuring-assignment,prefer-destructuring,react/prop-types */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import Paper from '@material-ui/core/Paper/Paper';
import Card from '@material-ui/core/Card/Card';
import Typography from '@material-ui/core/Typography';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';

import __ from '../lang/vi';
import Layout from '../components/Layout';
import withData from '../gql-lib/apollo';
import PersonalTable from '../components/PersonalTable';

const moment = require('moment');

moment.locale('vi');
const styles = {
  card: {
    width: '25%',
    marginTop: '1rem',
    textAlign: 'center',
  },
  header: {
    backgroundColor: '#fbfbfb',
  },
  content: {
    textAlign: 'center',
  },
  rank: {
    borderTop: '1px solid #dedfe0',
    borderBottom: '1px solid #dedfe0',
    fontSize: '1rem',
    '& > h2': {
      color: 'green',
    },
  },
  medals: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '1rem 0',
    '& > p': {
      width: '30%',
    },
  },
  medal: {
    width: '30%',
    '& .gold': {
      color: '#FDC824',
    },
    '& .silver': {
      color: '#E0DFE5',
    },
    '& .bronze': {
      color: '#EE9048',
    },
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
};
const MedalWithIcon = (props) => {
  const { type, number, className } = props;
  return (
    <span className={className}>
      <span className={type}>
        <li className="fa fa-medal" />
      </span>
      <span>{number}</span>
    </span>
  );
};

class User extends React.Component {
  static getInitialProps({ query: { username } }) {
    return { username };
  }

  render() {
    const { user } = this.props.data;
    const { classes } = this.props || {};
    if (!user) return <div>Loading</div>;
    return (
      <Layout title={__.common.Profile}>
        <Paper className="d-flex">
          <img className="mr-2" src={user.avatar} alt="avatar" />
          <div className="pt-4 pl-4">
            <h2 className="mb-4">{user.fullName}</h2>
            <p className="mt-2 mb-1">
              {user.job && (
                <span>
                  <span>{user.job.title}</span>
                  &nbsp;-&nbsp;
                  <span>{user.job.company}</span>
                </span>
              )}
            </p>
            <p className="mb-1">{user.address}</p>
            <p>
              <span>
                Tham gia&nbsp;
                {moment(user.createdAt).fromNow()}
              </span>
              <span>
                , lần cuối đăng nhập&nbsp;
                {moment(user.updatedAt).fromNow()}
              </span>
            </p>
          </div>
        </Paper>
        <Card className={classes.card}>
          <CardHeader title={__.common.Contests} className={classes.header} />
          <CardContent className={classes.rank}>
            <Typography component="h2">
              {user.rank ? user.rank : __.common.Unranked}
            </Typography>
          </CardContent>
          <CardContent className={classes.medals}>
            <MedalWithIcon
              className={classes.medal}
              type="gold"
              number={user.medals ? user.medals[0] : '0'}
            />
            <MedalWithIcon
              className={classes.medal}
              type="silver"
              number={user.medals ? user.medals[1] : '0'}
            />
            <MedalWithIcon
              className={classes.medal}
              type="bronze"
              number={user.medals ? user.medals[2] : '0'}
            />
          </CardContent>
        </Card>
        <PersonalTable data={[]} />
      </Layout>
    );
  }
}

const user = gql`
  query user($username: String!) {
    user(username: $username) {
      id
      fullName
      username
      avatar
      createdAt
      updatedAt
      contests
      medals
      rank
      bestContestRank
      job {
        title
        company
      }
      address
    }
  }
`;

export default withData(
  graphql(user, {
    options: (props) => ({
      variables: {
        username: props.username,
      },
    }),
    props: ({ data }) => ({
      data,
    }),
  })(withStyles(styles)(User)),
);
