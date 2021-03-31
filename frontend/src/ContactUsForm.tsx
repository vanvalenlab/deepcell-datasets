import { useForm } from 'react-hook-form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

export default function ContactUsForm() {
  const { register, errors, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    console.log('Name: ', data.name);
    console.log('Email: ', data.email);
    console.log('Subject: ', data.subject);
    console.log('Message: ', data.message);
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
                      message: 'Please use 30 characters or less'
                    }
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
                    pattern: /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/
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
                      message: 'Subject cannot exceed 75 characters'
                    }
                  })}
                  className='form-control formInput'
                  placeholder='Subject'
                ></input>
                {errors.subject && (
                  <span className='text-danger'>{errors.subject.message}</span>
                )}
              </Col>
            </Row>
            {/* Row 3 of form */}
            <Row className='py-2'>
              <Col>
                <textarea
                  rows={3}
                  name='message'
                  ref={register({
                    required: true
                  })}
                  className='form-control formInput'
                  placeholder='Message'
                ></textarea>
                {errors.message && <span className='text-danger'>Please enter a message</span>}
              </Col>
            </Row>
            <Button variant="dark" type="submit" className="w-50">Submit</Button>
          </form>
        </Col>
      </Row>
    </Container>
  );
}
