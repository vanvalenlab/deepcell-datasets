import { Link } from '@reach/router';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { MdSearch, MdSchool, MdNoteAdd } from 'react-icons/md';
import { ParallaxBanner } from 'react-scroll-parallax';

import Constants from './Constants';

export default function Landing() {

  return (
    <Container fluid className="px-0">

      {/* .gif banner */}
      <Row className="mx-auto">
        <ParallaxBanner style={{height: '450px'}} className="w-100 d-table" layers={[
            {
              image: '/images/combined.webp',
              amount: 0
            }
          ]}>
            <h1 className="text-light text-center display-3 d-table-cell align-middle position-sticky">
              A hub for biological images with single-cell annotations
            </h1>
          </ParallaxBanner>
      </Row>

      {/* feature icons */}
      <Row className="mx-auto mt-5">

        {/* section title */}
        {/* <Col xs={12} className="py-4"> */}
          {/* <h1 className="text-center">Browse Data</h1> */}
        {/* </Col> */}

        <Col xs={12} md={4} className="text-center mb-2">
          <MdNoteAdd size={70} />
          <h5>Contribute Data</h5>
          <p className="small">Expand DeepCell Datasets by uploading new images.</p>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <MdSearch size={70} />
          <h5>Browse Data</h5>
          <p className="small">Review and download our published datasets.</p>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2">
          <MdSchool size={70} />
          <h5>Learn More</h5>
          <p className="small">Learn more about the DeepCell.</p>
        </Col>
      </Row>

      {/* Buttons for the icons */}
      <Row className="mx-auto pb-3 mb-5">

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Link to={Constants.Contribute}>
            <Button variant="dark" className="w-75">
              Contribute
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Link to={Constants.Data}>
            <Button variant="dark" className="w-75">
              Browse
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Button variant="dark"  className="w-75" href="https://deepcell.org/about">
            Learn More
          </Button>
        </Col>

      </Row>
      
      {/* Parallax scroll image */}
      <Row className="mx-auto">
        <ParallaxBanner style={{height: '275px'}} layers={[
          {
            image: '/images/multiplex_overlay.webp',
            amount: 1
          }
        ]} />
      </Row>

      {/* Last Section */}
      <Row className="mx-auto pt-3 pb-5 mb-3 w-75">

        <Col xs={12} className="text-center py-4">
          <h1>Join Now</h1>
          <p className="small">Access and contribute to the collection of single-cell training data.</p>
        </Col>

        <Col xs={12} md={6} className="text-center mb-2 w-100">
          <Link to={Constants.SignUp}>
            <Button block variant="dark">
              Create an Account
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={6} className="text-center mb-2 w-100">
          <Link to={Constants.SignIn}>
            <Button block variant="dark">
              Login
            </Button>
          </Link>
        </Col>

      </Row>

    </Container>
  );
}
