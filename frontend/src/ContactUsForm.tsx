import { useState } from 'react';
import { useForm } from 'react-hook-form';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

const REACT_APP_SEND_EMAIL_API_ENDPOINT = process.env.REACT_APP_SEND_EMAIL_API_ENDPOINT || '';

export default function ContactUsForm() {
  const { register, errors, handleSubmit, reset } = useForm();
  const [successText, setSuccessText] = useState('');
  const [errorText, setErrorText] = useState('');

  const onSubmit = async (data) => {
    try {
      const payload = {
        name: data.name,
        email: data.email,
        subject: data.subject,
        message: data.message,
      };
      fetch(REACT_APP_SEND_EMAIL_API_ENDPOINT, {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: {
          'Content-Type': 'application/json',
        },
      })
        .then((res) => res.json())
        .then(
          (result) => {
            setSuccessText('Message Sent! Thanks for reaching out!');
            reset();
          },
          // Note: it's important to handle errors here
          // instead of a catch() block so that we don't swallow
          // exceptions from actual bugs in components.
          (error) => {
            setErrorText(error.toString());
          }
        );
    } catch (e) {
      setErrorText(e.toString());
    }
  };

  return (
    <Container>
      <Row>
        <Col xs={12} className='text-center'>
          <form id='contact-form' onSubmit={handleSubmit(onSubmit)} noValidate>
            {/* Row 1 of form */}
            <Row className='py-2'>
              <Col xs={6}>
                <input
                  type='text'
                  name='name'
                  ref={register({
                    required: { value: true, message: 'Please enter your name' },
                    maxLength: {
                      value: 30,
                      message: 'Please use 30 characters or less',
                    },
                  })}
                  className='form-control formInput'
                  placeholder='Name'
                ></input>
                {errors.name && <span className='text-danger'>{errors.name.message}</span>}
              </Col>
              <Col xs={6}>
                <input
                  type='email'
                  name='email'
                  ref={register({
                    required: true,
                    pattern: /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
                  })}
                  className='form-control formInput'
                  placeholder='Email address'
                ></input>
                {errors.email && (
                  <span className='text-danger'>Please enter a valid email address</span>
                )}
              </Col>
            </Row>
            {/* Row 2 of form */}
            <Row className='py-2'>
              <Col>
                <input
                  type='text'
                  name='subject'
                  ref={register({
                    required: { value: true, message: 'Please enter a subject' },
                    maxLength: {
                      value: 75,
                      message: 'Subject cannot exceed 75 characters',
                    },
                  })}
                  className='form-control formInput'
                  placeholder='Subject'
                ></input>
                {errors.subject && <span className='text-danger'>{errors.subject.message}</span>}
              </Col>
            </Row>
            {/* Row 3 of form */}
            <Row className='py-2'>
              <Col>
                <textarea
                  rows={3}
                  name='message'
                  ref={register({
                    required: true,
                  })}
                  className='form-control formInput'
                  placeholder='Message'
                ></textarea>
                {errors.message && <span className='text-danger'>Please enter a message</span>}
              </Col>
            </Row>
            {successText.length > 0 && (
              <Row>
                <Col xs={12}>
                  <Alert variant='success' onClose={() => setSuccessText('')} dismissible>
                    {successText}
                  </Alert>
                </Col>
              </Row>
            )}
            {errorText.length > 0 && (
              <Row>
                <Col xs={12}>
                  <Alert variant='danger' onClose={() => setErrorText('')} dismissible>
                    {errorText}
                  </Alert>
                </Col>
              </Row>
            )}
            <Button variant='dark' type='submit' className='w-50'>
              Submit
            </Button>
          </form>
        </Col>
      </Row>
    </Container>
  );
}
