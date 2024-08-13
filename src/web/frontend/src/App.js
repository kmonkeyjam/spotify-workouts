import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://d27hv4mf8axlyg.cloudfront.net/api/graphql',
  cache: new InMemoryCache(),
  headers: {
    Authorization: `Bearer ${document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1")}`
  }
});

const IS_LOGGED_IN = gql`
  query IsLoggedIn {
    login_status {
      is_logged_in
      login_url
    }
  }
`;

function AuthStatus() {
  const { loading, error, data } = useQuery(IS_LOGGED_IN);

  if (loading) return <p>Loading...</p>;
  if (error || !data.login_status.is_logged_in) {
    return (
      <button onClick={() => window.location.href = '/login'}>
        Login
      </button>
    );
  }
  const { is_logged_in, login_url } = data.login_status;

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

