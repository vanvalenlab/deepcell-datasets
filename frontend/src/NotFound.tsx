import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
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
