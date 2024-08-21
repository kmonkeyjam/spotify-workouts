import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://d27hv4mf8axlyg.cloudfront.net/api/graphql',
  cache: new InMemoryCache(),
});

const IS_LOGGED_IN = gql`
  query IsLoggedIn($token: String!) {
    login_status(token: $token) {
      is_logged_in
      login_url
    }
  }
`;

function AuthStatus() {
  const token = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
  const { loading, error, data } = useQuery(IS_LOGGED_IN, {
    variables: { token },
  });

  if (loading) return <p>Loading...</p>;
  if (error || !data.login_status.is_logged_in) {
    return (
      <button onClick={() => window.location.href = data.login_status.login_url}>
        Login
      </button>
    );
  }
  const { is_logged_in, login_url } = data.login_status;

  return is_logged_in ? <p>Logged In</p> : <a href={login_url}>Login</a>;
}

function App() {
  return (
    <ApolloProvider client={client}>
      <AuthStatus />
    </ApolloProvider>
  );
}

export default App;
