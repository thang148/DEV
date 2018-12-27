import React from 'react';

import Layout from '../components/Layout';
import Contests from '../containers/Contests';
import withData from '../gql-lib/apollo';

const Index = () => (
  <Layout title="Aivivn">
    <Contests />
  </Layout>
);
export default withData(Index);
