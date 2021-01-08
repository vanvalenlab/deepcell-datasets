import { useState } from 'react';
import { useNavigate, useParams } from '@reach/router'
import { Auth } from '@aws-amplify/auth';
import styled from 'styled-components';
import { Alert, Button, Container, Form } from 'react-bootstrap';
import Constants from '../Constants';

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
  const [error, setError] = useState(null);
  const [isClicked, setIsClicked] = useState(false);
  const [isResent, setIsResent] = useState(false);

  const resendConfirmationCode = async () => {
    try {
      await Auth.resendSignUp(email);
      setIsResent(true);
    } catch (err) {
      setError(err.message);
    }
  }

  const handleSubmit = async (e: any) => {
    setIsClicked(true);
    e.preventDefault();
    if (code.length === 0) {
      e.stopPropagation();
      setIsClicked(false);
      return;
    }

    try {
      await Auth.confirmSignUp(email, code);
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
          Confirmation Code resent to your email.
        </Alert>
        : null
      }

      <Container className="text-center mb-3 py-3 bg-light border rounded">

        <Form className="text-left" onSubmit={handleSubmit}>
          <Form.Group controlId="formBasicEmail">
            <Form.Label className="font-weight-bold small">Email address</Form.Label>
            <Form.Control required readOnly type="email" defaultValue={email} />
          </Form.Group>

          <Form.Group controlId="formBasicPassword">
            <Form.Label className="font-weight-bold small">Confirmation Code</Form.Label>
            <Form.Control required type="text" placeholder="Enter your code" onChange={e => setCode(e.target.value)} />
          </Form.Group>

          <Button variant="success" type="submit" block>
            Confirm
          </Button>
        </Form>
      </Container>
      <Container className="text-center py-1 border rounded">
        <div className="m-2">
          Lost your code?
          <br />
          <Button variant="link" size="sm" onClick={resendConfirmationCode}>Resend code.</Button>
        </div>
      </Container>
    </MaxWidthDiv>
  );
}