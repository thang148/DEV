/* eslint-disable max-len,react/destructuring-assignment,react/forbid-prop-types */
import AppBar from '@material-ui/core/AppBar';
import Tab from '@material-ui/core/Tab';
import Tabs from '@material-ui/core/Tabs';
import Typography from '@material-ui/core/Typography';
import gql from 'graphql-tag';
import Link from 'next/link';
import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { graphql } from 'react-apollo';

import Layout from '../components/Layout';
import LeaderBoard from '../components/LeaderBoard';
import Overview from '../components/Overview';
import Submisssion from '../components/Submission';
import withData from '../gql-lib/apollo';
import __ from '../lang/vi';

const TabContainer = (props) => (
  <Typography component="div" style={{ padding: 8 * 3, minHeight: '500px' }}>
    {props.children}
  </Typography>
);
TabContainer.propTypes = {
  children: PropTypes.node.isRequired,
};

class Contest extends Component {
  state = {
    value: 0,
  };

  static getInitialProps({ query: { id } }) {
    return { id };
  }

  handleChange = (event, value) => {
    this.setState({ value });
  };

  render() {
    const { value } = this.state;
    const { contest } = this.props.data;
    return (
      <Layout title={`Contest - ${contest && contest.title}`}>
        {contest ? (
          <div className="root">
            <h1>{contest.title}</h1>
            <p>{contest.subtitle}</p>
            <AppBar position="static" color="default">
              <Tabs
                value={value}
                onChange={this.handleChange}
                indicatorColor="primary"
                textColor="primary"
                scrollable
                scrollButtons="auto"
              >
                <Tab label={__.common.Overview} />
                <Tab label={__.common.Data} />
                <Tab label={__.common.Discussion} />
                <Tab label={__.common.LeaderBoard} />
                <Tab label={__.common.Rule} />
                <Tab label={__.common.Upload} />
              </Tabs>
            </AppBar>
            {value === 0 && (
              <TabContainer>
                <Overview contest={contest} />
              </TabContainer>
            )}
            {value === 1 && (
              <TabContainer>
                <Link href={contest.data.name}>
                  <a>
                    <i className="fas fa-file-download pr-2" />
                    {contest.data.name}
                  </a>
                </Link>
              </TabContainer>
            )}
            {value === 2 && <TabContainer>Thảo luận</TabContainer>}
            {value === 3 && (
              <TabContainer>
                <LeaderBoard teams={contest.teams} />
              </TabContainer>
            )}
            {value === 4 && <TabContainer>Luật chơi</TabContainer>}
            {value === 5 && (
              <TabContainer>
                <Submisssion contestId={contest.id} />
              </TabContainer>
            )}
          </div>
        ) : null}
        <style jsx>
          {`
            .root {
              background: #fff;
            }
          `}
        </style>
      </Layout>
    );
  }
}

Contest.propTypes = {
  data: PropTypes.object.isRequired,
};
const CONTEST_QUERY = gql`
  query contest($id: ID!) {
    contest(id: $id) {
      id
      title
      subtitle
      updatedAt
      status
      numTeams
      numSubmissions
      description
      evaluation
      prizes
      timeline
      weight
      teams {
        total
        items {
          id
          name
          publicScore
          change
          numSubmissions
          lastSubmissionAt
          members {
            id
            # fullName
            username
            avatar
            user {
              avatar
            }
          }
        }
      }
      myTeam {
        id
      }
      data {
        name
        link
      }
    }
  }
`;

export default withData(
  graphql(CONTEST_QUERY, {
    options: (props) => ({
      variables: {
        id: props.id,
      },
    }),
    props: ({ data }) => ({
      data,
    }),
  })(Contest),
);
