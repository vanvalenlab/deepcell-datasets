import { useState } from 'react';
import { Link, Redirect } from '@reach/router';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import { Auth } from '@aws-amplify/auth';
import styled from 'styled-components';
import Constants from '../Constants';

const MaxWidthDiv = styled.div`
  max-width: 350px;
`;

export default function Login () {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isClicked, setIsClicked] = useState(false);
  const [error, setError] = useState(null);
  const [redirect, setRedirect] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setIsClicked(true);
    if (username.length === 0 || password.length === 0) {
      e.stopPropagation();
      setIsClicked(false);
      return;
    }

    try {
      await Auth.signIn(username, password);
      setRedirect(true);
    } catch (err) {
      setError(err.message);
      setIsClicked(false);
    }
  };

  return (
    <MaxWidthDiv className="py-4 mx-auto">
      <h2 className="text-center">Sign in to DeepCell Datasets</h2>

      { (error !== null) ?
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
        : null
      }

      <Container className="text-center mb-3 py-3 bg-light border rounded">      
        <Form className="text-left" onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicEmail">
            <Form.Label className="font-weight-bold small">Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email" onChange={e => setUsername(e.target.value)} />
          </Form.Group>

          <Form.Group controlId="formBasicPassword">
            <Form.Label className="font-weight-bold small">Password</Form.Label>
            <Form.Control type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
            <Link to={Constants.ForgotPassword} className="small">Forgot your password?</Link>
          </Form.Group>
          <Button variant="success" type="submit" block disabled={isClicked}>
            { isClicked ? "Signing In..." : "Sign in" }
          </Button>
        </Form>
      </Container>
      <Container className="text-center py-1 border rounded">
        <div className="m-2">
          Don't have an account?
          <br />
          <Link to={Constants.SignUp}>Create an account</Link>.
        </div>
      </Container>
      {redirect && <Redirect to={Constants.Data} noThrow />}
    </MaxWidthDiv>
  );
}
