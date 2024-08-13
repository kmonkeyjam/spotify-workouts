import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://vhomhw0wvg.execute-api.us-west-2.amazonaws.com/api/graphql',
  cache: new InMemoryCache(),
  headers: {
    Authorization: `Bearer ${document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1")}`
  }
});

const IS_LOGGED_IN = gql`
  query IsLoggedIn($token: String!) {
    isLoggedIn(token: $token)
  }
`;

function AuthStatus() {
  const { loading, error, data } = useQuery(IS_LOGGED_IN);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  return data.isLoggedIn ? <p>Logged In</p> : <p>Logged Out</p>;
}

function App() {
  return (
    <ApolloProvider client={client}>
      <AuthStatus />
    </ApolloProvider>
  );
}

export default App;

