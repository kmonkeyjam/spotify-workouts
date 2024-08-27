import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';
import { useIsLoggedInQuery } from './generated/graphql'; 

// Apollo Client setup
const client = new ApolloClient({
  uri: 'https://d27hv4mf8axlyg.cloudfront.net/api/graphql',
  cache: new InMemoryCache(),
});

const AuthStatus: React.FC = () => {
  // Retrieve the token from the cookies
  const token = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1") || "";

  // Use the useQuery hook with types for the data and variables
  const { loading, error, data } = useIsLoggedInQuery({
    variables: { token : "foobar" },
  });

  // Handling loading state
  if (loading) return <p>Loading...</p>;

  // Handling error or not logged in state
  if (error || !data?.login_status?.is_logged_in) {
    return (
      <button onClick={() => window.location.href = data?.login_status?.login_url || ''}>
        Login
      </button>
    );
  }

  // Destructure the needed data
  const { is_logged_in, login_url } = data.login_status;

  return is_logged_in ? <p>Logged In</p> : <a href={login_url || ""}>Login</a>;
};

const App: React.FC = () => {
  return (
    <ApolloProvider client={client}>
      <AuthStatus />
    </ApolloProvider>
  );
};

export default App;
