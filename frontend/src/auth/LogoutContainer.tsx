import { useState } from 'react';
import { Redirect } from '@reach/router';
import Spinner from 'react-bootstrap/Spinner'
import { Auth } from '@aws-amplify/auth';
import Constants from '../Constants';

export default function LogoutContainer() {

  const [isLoggedOut, setIsLoggedOut] = useState(false)

  const signOut = async () => {
    try {
      await Auth.signOut();
      setIsLoggedOut(true);
    } catch (e) {
      console.log('error during logout', e);
      setIsLoggedOut(false);
    }
  };

  signOut();

  return (
    isLoggedOut ? <Redirect to={Constants.Index} noThrow /> :
      <Spinner animation="border" role="status">
        <span className="sr-only">Loading...</span>
      </Spinner>
  );
}