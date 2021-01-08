import { useState } from 'react';
import { Link, useNavigate } from '@reach/router';
import { Alert, Button, Container, Form } from 'react-bootstrap';
import { Auth } from '@aws-amplify/auth';
import styled from 'styled-components';
import Constants from '../Constants';
import PasswordSchema from './PasswordSchema';

const MaxWidthDiv = styled.div`
  max-width: 880px;
`;

const eduRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+edu))$/i;

export default function SignUpContainer() {
  const navigate = useNavigate();
  const [validated, setValidated] = useState(false);
  const [email, setEmail] = useState('');
  const [isValidEmail, setIsValidEmail] = useState<boolean|undefined>(true);
  const [password, setPassword] = useState('');
  const [isValidPassword, setIsValidPassword] = useState<boolean|undefined>(true);
  const [agreedToTerms, setAgreedToTerms] = useState<boolean>(false);
  const [isClicked, setIsClicked] = useState(false);
  const [error, setError] = useState(null);

  const handleEmailChange = (e: any) => {
    const value = e.target.value;
    setEmail(value);
    if (value.length === 0) {
      setIsValidEmail(undefined);
    } else if (eduRegEx.test(value)) {
      setIsValidEmail(true);
    } else {
      setIsValidEmail(false);
    }
  };

  const handlePasswordChange = (e: any) => {
    const value = e.target.value;
    setPassword(value);
    if (value.length === 0) {
      setIsValidPassword(undefined);
    } else if (PasswordSchema.validate(value)) {
      setIsValidPassword(true);
    } else {
      setIsValidPassword(false);
    }
  };

  const handleSubmit = async (e: any) => {
    setIsClicked(true);
    e.preventDefault();
    if (!isValidEmail || !isValidPassword || !agreedToTerms) {
      e.stopPropagation();
      setValidated(false);
      setIsClicked(false);
      return;
    }

    setValidated(true);

    try {
      const res = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
          email: email
        }
      });
      if (res.userConfirmed) {
        navigate(`/profile`);
      } else {
        navigate(`/verify/${email}`);
      }
    } catch (err) {
      setError(err.message);
      setIsClicked(false);
    }

  };

  return (
    <MaxWidthDiv className="mx-auto">
      <Container className="text-center py-4 w-75">
        <h6 className="text-muted">Join DeepCell Datasets</h6>
        <h1>Create your account</h1>

        { (error !== null) ?
          <Alert variant="danger" dismissible onClose={() => setError(null)}>
            {error}
          </Alert>
          : null
        }

        <Form noValidate validated={validated} onSubmit={handleSubmit} className="text-left">
          <Form.Group controlId="formEmail">
            <Form.Label className="font-weight-bold small">Email address<span className="text-danger">*</span></Form.Label>
            <Form.Control required type="email" placeholder="Enter email"
              onChange={handleEmailChange}
              isInvalid={email.length > 0 && !isValidEmail}
              isValid={email.length > 0 && isValidEmail} />
            <Form.Text muted>
              Enter a valid .edu email address.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="formPassword">
            <Form.Label className="font-weight-bold small">Password<span className="text-danger">*</span></Form.Label>
            <Form.Control required type="password" placeholder="Password"
              onChange={handlePasswordChange}
              isInvalid={password.length > 0 && !isValidPassword}
              isValid={password.length > 0 && isValidPassword} />
            <Form.Text id="passwordHelpBlock" muted>
              Your password must be between 8 and 128 characters and contain a digit an uppercase letter, and a lowercase letter.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="formTermsAndConditions">
            <Form.Check inline required type="checkbox" onChange={e => setAgreedToTerms(!agreedToTerms)} />
            <Form.Label className="font-weight-bold small">I agree to the <Link to={Constants.Terms}>Terms & Conditions</Link>.<span className="text-danger">*</span></Form.Label>
          </Form.Group>

          <Button variant="primary" type="submit" disabled={isClicked}>
            { isClicked ? "Submitting..." : "Submit" }
          </Button>
          <div className="pt-2">
            <Link to={Constants.SignIn}>Already have an account?</Link>
          </div>
        </Form>
      </Container>
    </MaxWidthDiv>
  );
}
