import React, { useState } from 'react';
import { useNavigate } from '@reach/router';
import { Alert, Button, Container, Form } from 'react-bootstrap';
import { Auth } from '@aws-amplify/auth';
import styled from 'styled-components';

const MaxWidthDiv = styled.div`
  max-width: 350px;
`;

export default function ForgotPasswordContainer () {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [isClicked, setIsClicked] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setIsClicked(true);
    if (email.length === 0) {
      e.stopPropagation();
      setIsClicked(false);
      return;
    }

    try {
      await Auth.forgotPassword(email);
      navigate(`/reset/${email}`); // TODO: template Constants.ResetEmail ?
    } catch (err) {
      setError(err.message);
    }
    setIsClicked(false);
  };

  return (
    <MaxWidthDiv className="pt-4 mx-auto">
      <h2 className="text-center">Reset your password</h2>

      { (error !== null) ?
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
        : null
      }

      <Container className="text-center mb-3 py-3 bg-light border rounded">

        <div className="font-weight-bold small pb-2">
          Enter your user account's verified email address and we will send you a password reset link.
        </div>
        <Form className="text-left" onSubmit={handleSubmit}>
          <Form.Group controlId="resetPasswordEmail">
            <Form.Control type="email" placeholder="Enter email" onChange={e => setEmail(e.target.value)} />
          </Form.Group>
          <Button variant="success" type="submit" block disabled={isClicked}>
            { isClicked ? "Sending..." : "Send password reset email" }
          </Button>
        </Form>

      </Container>
    </MaxWidthDiv>
  );
}
