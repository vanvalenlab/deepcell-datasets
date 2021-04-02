import { useState } from 'react';
import { Link, useNavigate } from '@reach/router';
import { Auth } from '@aws-amplify/auth';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal'
import styled from 'styled-components';
import Constants from '../Constants';
import PasswordSchema from './PasswordSchema';
import TermsAndConditions from '../TermsAndConditions';

const MaxWidthDiv = styled.div`
  max-width: 880px;
`;

const DOMAIN_WHITELIST = process.env.REACT_APP_DOMAIN_WHITELIST || '.edu';

const testEmail = (email) => {
  // check that the input string is an well formed email
  email = email.toString().toLowerCase();
  const emailFilter = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+.)+([a-zA-Z0-9]{2,4})+$/;
  if (!emailFilter.test(email)) {
    return false;
  }

  const whitelist = DOMAIN_WHITELIST.split(',');
  for (let s of whitelist) {
    if (email.endsWith(s)) {
      return true;
    }
  } 
  // email is well formed but not in the whitelist
  return false;
};

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

  const [showTOC, setShowTOC] = useState(false);

  const handleEmailChange = (e: any) => {
    const value = e.target.value;
    setEmail(value);
    if (value.length === 0) {
      setIsValidEmail(undefined);
    } else if (testEmail(value)) {
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
        navigate(Constants.Data);
      } else {
        navigate(`${Constants.ConfirmEmail}/${email}`);
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
              Your password must be between 8 and 128 characters and contain a digit, an uppercase letter, a lowercase letter, and a special character.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="formTermsAndConditions">
            <Form.Check inline required type="checkbox" onChange={e => setAgreedToTerms(!agreedToTerms)} />
            <Form.Label className="font-weight-bold small">
              {/* eslint-disable-next-line */} 
              I agree to the <a href="#" onClick={() => setShowTOC(true)}>Terms & Conditions</a>.<span className="text-danger">*</span>
            </Form.Label>
          </Form.Group>

          <Modal
            show={showTOC}
            onHide={() => setShowTOC(false)}
            backdrop="static"
            size="lg"
          >
            <Modal.Header closeButton />
            <Modal.Body>
              <TermsAndConditions />
            </Modal.Body>
            <Modal.Footer>
              <Button variant="secondary" onClick={() => setShowTOC(false)}>
                Close
              </Button>
            </Modal.Footer>
          </Modal>

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
