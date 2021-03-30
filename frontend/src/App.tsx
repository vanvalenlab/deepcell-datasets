import { useEffect, useState, lazy, Suspense } from 'react';
import { Redirect, Router, RouteComponentProps } from '@reach/router'
import { Amplify, Hub } from '@aws-amplify/core';
import { Auth } from '@aws-amplify/auth';
import { ParallaxProvider } from 'react-scroll-parallax';
import  styled  from  'styled-components';

import Constants from './Constants';
import LoadingPage from './LoadingPage';

const NavigationToolbar = lazy(() => import('./NavigationToolbar'));
const Footer = lazy(() => import('./Footer'));
const SignUpContainer = lazy(() => import('./auth/SignUpContainer'));
const LoginContainer = lazy(() => import('./auth/LoginContainer'));
const LogoutContainer = lazy(() => import('./auth/LogoutContainer'));
const ConfirmEmailContainer = lazy(() => import('./auth/ConfirmEmailContainer'));
const ForgotPasswordContainer = lazy(() => import('./auth/ForgotPasswordContainer'));
const PasswordResetContainer = lazy(() => import('./auth/PasswordResetContainer'));
const Landing = lazy(() => import('./Landing'));
const Data = lazy(() => import('./datasets/Data'));
const Contribute = lazy(() => import('./datasets/Contribute'));
const PrivacyPolicy = lazy(() => import('./PrivacyPolicy'));
const TermsAndConditions = lazy(() => import('./TermsAndConditions'));
const NotFound = lazy(() => import('./NotFound'));

const RouterPage = (
  props: { pageComponent: JSX.Element } & RouteComponentProps
) => props.pageComponent;

const AnonymousRouterPage = (
  props: { pageComponent: JSX.Element, isLoggedIn: boolean } & RouteComponentProps
) => {
  const { ...rest } = props; // eslint-disable-line
  return props.isLoggedIn ? <Redirect to={Constants.Data} noThrow /> : props.pageComponent;
};

const ProtectedRouterPage = (
  props: { pageComponent: JSX.Element, isLoggedIn: boolean } & RouteComponentProps
) => {
  const { ...rest } = props; // eslint-disable-line
  return props.isLoggedIn ? props.pageComponent : <Redirect to={Constants.SignIn} noThrow />;
};

const Root = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

const Main = styled.main`
  flex-grow: 1;
`;

export default function App() {

  /**
   * Currently authentication happens here and the user is propogated into each
   * of the components in the routes. Another method that would provide the
   * rest of the components with more user information would be using a 
   * UserContext and UserProvider.
   * 
   * A couple examples:
   * https://itnext.io/creating-reusable-abstractions-with-amplify-and-react-hooks-97784c8b5c2a
   * https://www.rockyourcode.com/custom-react-hook-use-aws-amplify-auth/
   */
  useEffect(() => {
    Amplify.configure({
      Auth: {
        region: process.env.REACT_APP_REGION,
        identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID,
        userPoolId: process.env.REACT_APP_USER_POOL_ID,
        userPoolWebClientId: process.env.REACT_APP_USER_POOL_WEB_CLIENT_ID,
        authenticationFlowType: 'USER_SRP_AUTH',
      },
      Storage: {
        AWSS3: {
          bucket: process.env.REACT_APP_S3_BUCKET,
          region: process.env.REACT_APP_REGION
        }
      }
    });
  }, []);

  const [user, setUser] = useState(null)

  const updateUser = async () => {
    try {
      const currUser = await Auth.currentAuthenticatedUser();
      setUser(currUser);
    } catch (e) {
      setUser(null);
    }
  };

  useEffect(() => {
    Hub.listen('auth', updateUser); // listen for login/signup events
    updateUser(); // check manually the first time because we won't get a Hub event
    return () => Hub.remove('auth', updateUser); // cleanup
  }, []);

  return (
    <Root>
      <Suspense fallback={<LoadingPage />}>
        <NavigationToolbar isLoggedIn={user !== null} />
        <ParallaxProvider>
          <Main>
            <Router>
              <RouterPage path={Constants.Index} pageComponent={<Landing />} />
              <RouterPage path={Constants.Terms} pageComponent={<TermsAndConditions />} />
              <RouterPage path={Constants.Privacy} pageComponent={<PrivacyPolicy />} />
              <RouterPage path={Constants.SignOut} pageComponent={<LogoutContainer />} />
              <RouterPage path={Constants.ForgotPassword} pageComponent={<ForgotPasswordContainer />} />
              <RouterPage path={`${Constants.ResetPassword}/:email`} pageComponent={<PasswordResetContainer />} />
              <RouterPage path={Constants.Contribute} pageComponent={<Contribute />} />
              {/* Pages only accessible when logged in */}
              <ProtectedRouterPage path={Constants.Data} isLoggedIn={user !== null} pageComponent={<Data />} />
              {/* Pages only accessible when NOT logged in */}
              <AnonymousRouterPage path={`${Constants.ConfirmEmail}/:email`} isLoggedIn={user !== null} pageComponent={<ConfirmEmailContainer />} />
              <AnonymousRouterPage path={Constants.SignIn} isLoggedIn={user !== null} pageComponent={<LoginContainer />} />
              <AnonymousRouterPage path={Constants.SignUp} isLoggedIn={user !== null} pageComponent={<SignUpContainer />} />
              <RouterPage default pageComponent={<NotFound />} />
            </Router>
          </Main>
        </ParallaxProvider>
        <Footer />
      </Suspense>
    </Root>
  );
};
