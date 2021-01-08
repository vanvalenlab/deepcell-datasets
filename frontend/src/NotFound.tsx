import { Button, Col, Container, Row } from 'react-bootstrap';
import Constants from './Constants';

export default function NotFound() {
  return (
    <Container className='pt-5'>
      <Row>
        <Col className='text-center'> 
          <h1>Oops!</h1>
          <h3>404 Not Found</h3>
          <p>
            Sorry, an error has occured, Requested page not found!
          </p>
          <Button variant="primary" href={Constants.Index}>
            Take Me Home
          </Button>
        </Col>
      </Row>
    </Container>
  );
}
