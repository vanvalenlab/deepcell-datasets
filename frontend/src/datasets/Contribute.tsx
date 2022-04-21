// import { useState } from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import ContactUsForm from '../ContactUsForm';

export default function Contribute() {
  return (
    <Container fluid>
      <Row className='text-center py-4'>
        <Col xs={12}>
          <h1>Contribute Data</h1>
        </Col>
      </Row>

      <Row className='text-center py-4'>
        <Col xs={12} md={{ span: 8, offset: 2 }}>
          <Container>
            <span>
              We are hard at work on an easy way to upload data and register it with DeepCell
              Datasets! In the mean-time, if you would like to contribute data, please reach out to
              us and we will work with you on the best way to add your data.
            </span>
          </Container>
        </Col>
      </Row>

      <Row className='mx-auto pb-2'>
        <Col xs={12} md={{ span: 8, offset: 2 }}>
          <ContactUsForm />
        </Col>
      </Row>
    </Container>
  );
}
