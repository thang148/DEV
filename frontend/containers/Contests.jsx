import gql from 'graphql-tag';
import React from 'react';
import { graphql } from 'react-apollo';

import ContestCard from '../components/ContestCard';

const POSTS_PER_PAGE = 5;

// eslint-disable-next-line
function Contests({ data: { loading, contests }, loadMore }) {
  // if (error) return <div>{{ error }}</div>;
  return (
    <div className="contests">
      {loading ? (
        <div> Loading </div>
      ) : (
        contests &&
        contests.map((contest) => (
          <ContestCard key={contest.id} contest={contest} />
        ))
      )}
      <button type="button" onClick={() => loadMore()}>
        Load More
      </button>
    </div>
  );
}

const CONTESTS = gql`
  query contests($skip: Int!, $take: Int!) {
    contests(skip: $skip, take: $take) {
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
      }
      myTeam {
        id
      }
    }
  }
`;

export default graphql(CONTESTS, {
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
        skip: data.contests.length,
      },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult) {
          return previousResult;
        }
        return Object.assign({}, previousResult, {
          // Append the new posts results to the old one
          contests: [...previousResult.contests, ...fetchMoreResult.contests],
        });
      },
    }),
  }),
})(Contests);
