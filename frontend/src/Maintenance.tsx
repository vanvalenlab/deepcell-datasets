import { Link } from '@reach/router';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import Constants from './Constants';

export default function Maintenance() {

  return (
    <Container>
      <Row className="mx-auto">
        <Col xs={12}>
          <h1 className="text-center display-3 d-table-cell align-middle position-sticky">
            This page is currently under development!
          </h1>
        </Col>
      </Row>

      <Row className="mx-auto pt-5">
        <Col xs={12}>
          <Link to={Constants.Index}>
            <Button block variant="dark">
              Home
            </Button>
          </Link>
        </Col>
      </Row>
    </Container>
  );
}
