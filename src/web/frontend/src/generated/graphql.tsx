import { gql } from '@apollo/client';
import * as Apollo from '@apollo/client';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
const defaultOptions = {} as const;
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
};

export type LoginStatus = {
  __typename?: 'LoginStatus';
  is_logged_in: Scalars['Boolean']['output'];
  login_url?: Maybe<Scalars['String']['output']>;
  name?: Maybe<Scalars['String']['output']>;
};

export type Query = {
  __typename?: 'Query';
  login_status?: Maybe<LoginStatus>;
};


export type QueryLogin_StatusArgs = {
  token?: InputMaybe<Scalars['String']['input']>;
};

export type IsLoggedInQueryVariables = Exact<{
  token?: InputMaybe<Scalars['String']['input']>;
}>;


export type IsLoggedInQuery = { __typename?: 'Query', login_status?: { __typename?: 'LoginStatus', is_logged_in: boolean, login_url?: string | null, name?: string | null } | null };


export const IsLoggedInDocument = gql`
    query IsLoggedIn($token: String) {
  login_status(token: $token) {
    is_logged_in
    login_url
    name
  }
}
    `;

/**
 * __useIsLoggedInQuery__
 *
 * To run a query within a React component, call `useIsLoggedInQuery` and pass it any options that fit your needs.
 * When your component renders, `useIsLoggedInQuery` returns an object from Apollo Client that contains loading, error, and data properties
 * you can use to render your UI.
 *
 * @param baseOptions options that will be passed into the query, supported options are listed on: https://www.apollographql.com/docs/react/api/react-hooks/#options;
 *
 * @example
 * const { data, loading, error } = useIsLoggedInQuery({
 *   variables: {
 *      token: // value for 'token'
 *   },
 * });
 */
export function useIsLoggedInQuery(baseOptions?: Apollo.QueryHookOptions<IsLoggedInQuery, IsLoggedInQueryVariables>) {
        const options = {...defaultOptions, ...baseOptions}
        return Apollo.useQuery<IsLoggedInQuery, IsLoggedInQueryVariables>(IsLoggedInDocument, options);
      }
export function useIsLoggedInLazyQuery(baseOptions?: Apollo.LazyQueryHookOptions<IsLoggedInQuery, IsLoggedInQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useLazyQuery<IsLoggedInQuery, IsLoggedInQueryVariables>(IsLoggedInDocument, options);
        }
export function useIsLoggedInSuspenseQuery(baseOptions?: Apollo.SuspenseQueryHookOptions<IsLoggedInQuery, IsLoggedInQueryVariables>) {
          const options = {...defaultOptions, ...baseOptions}
          return Apollo.useSuspenseQuery<IsLoggedInQuery, IsLoggedInQueryVariables>(IsLoggedInDocument, options);
        }
export type IsLoggedInQueryHookResult = ReturnType<typeof useIsLoggedInQuery>;
export type IsLoggedInLazyQueryHookResult = ReturnType<typeof useIsLoggedInLazyQuery>;
export type IsLoggedInSuspenseQueryHookResult = ReturnType<typeof useIsLoggedInSuspenseQuery>;
export type IsLoggedInQueryResult = Apollo.QueryResult<IsLoggedInQuery, IsLoggedInQueryVariables>;