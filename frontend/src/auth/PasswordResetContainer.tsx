import { useState } from 'react';
import { useNavigate, useParams } from '@reach/router'
import { Auth } from '@aws-amplify/auth';
import styled from 'styled-components';
import { Alert, Button, Container, Form } from 'react-bootstrap';
import Constants from '../Constants';
import PasswordSchema from './PasswordSchema';

const MaxWidthDiv = styled.div`
  max-width: 350px;
`;

export default function ConfirmEmailContainer() {
  const navigate = useNavigate();
  const params = useParams()
  const email = params?.email;

  if (email === undefined || email === null || email.length === 0) {
      // invalid - just redirect to home
      navigate(Constants.Index);
  }

  const [code, setCode] = useState<string>('');
  const [password, setPassword] = useState('');
  const [isValidPassword, setIsValidPassword] = useState<boolean|undefined>(true);
  const [error, setError] = useState(null);
  const [isClicked, setIsClicked] = useState(false);
  const [isResent, setIsResent] = useState(false);

  const resendResetCode = async () => {
    try {
      await Auth.forgotPassword(email);
      setIsResent(true);
    } catch (err) {
      setError(err.message);
    }
  }

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
    if (code.length === 0) {
      e.stopPropagation();
      setIsClicked(false);
      return;
    }

    try {
      await Auth.forgotPasswordSubmit(email, code, password);
      navigate(Constants.Data);
    } catch (err) {
      setError(err.message);
      setIsClicked(false);
    }
  };

  return (
    <MaxWidthDiv className="pt-4 mx-auto">
      <h2 className="text-center">Confirm your Email</h2>

      { (error !== null) ?
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
        : null
      }

      { (isResent) ?
        <Alert variant="success" dismissible onClose={() => setIsResent(false)}>
          Email sent.
        </Alert>
        : null
      }

      <Container className="text-center mb-3 py-3 bg-light border rounded">

        <Form className="text-left" onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicEmail">
            <Form.Label className="font-weight-bold small">Email address</Form.Label>
            <Form.Control required readOnly type="email" defaultValue={email} />
          </Form.Group>

          <Form.Group controlId="formBasicCode">
            <Form.Label className="font-weight-bold small">Confirmation Code</Form.Label>
            <Form.Control required type="text" placeholder="Enter your code" onChange={e => setCode(e.target.value)} />
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

          <Button variant="success" type="submit" block>
            { isClicked ? "Submitting..." : "Submit" }
          </Button>
        </Form>

      </Container>
      <Container className="text-center py-1 border rounded">
        <div className="m-2">
          Didn't get the email?
          <br />
          <Button variant="link" size="sm" onClick={resendResetCode}>Resend email.</Button>
        </div>
      </Container>
    </MaxWidthDiv>
  );
}