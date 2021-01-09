import { Link } from '@reach/router';

import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { MdInsertDriveFile, MdPhoto, MdPhotoLibrary } from 'react-icons/md';
import { ParallaxBanner } from 'react-scroll-parallax';
import styled from 'styled-components';

import Constants from './Constants';

const ImageBanner = styled.div`
  min-height: 380px;
  background: url(/images/combined.gif) no-repeat center center;
  background-size: cover;
`;

export default function Landing() {

  return (
    <Container fluid className="px-0">

      {/* .gif banner */}
      <Row className="mx-auto">
        <ImageBanner className="w-100 d-table">
          <h1 className="px-5 text-light text-center display-3 d-table-cell align-middle">
            A hub for biological images with single-cell annotations
          </h1>
        </ImageBanner>
      </Row>

      {/* feature icons */}
      <Row className="mx-auto">

        {/* section title */}
        <Col xs={12} className="py-4">
          <h1 className="text-center">Browse Data</h1>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <MdInsertDriveFile size={70} />
          <h5>Training Data</h5>
          <p className="small">Review and download published training datasets.</p>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2">
          <MdPhotoLibrary size={70} />
          <h5>Experiments</h5>
          <p className="small">Explore the samples in published experiments.</p>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2">
          <MdPhoto size={70} />
          <h5>Samples</h5>
          <p className="small">Query and download individual biological images.</p>
        </Col>
      </Row>

      {/* Buttons for the icons */}
      <Row className="mx-auto pb-4 mb-3">

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Link to="/training">
            <Button variant="dark" className="w-75">
              Browse Training Data
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Link to="/experiments">
            <Button variant="dark" className="w-75">
              Browse Experiments
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center w-100 mb-2">
          <Link to="/samples" className="w-50">
            <Button variant="dark" className="w-75">
              Browse Samples
            </Button>
          </Link>
        </Col>

      </Row>
      
      {/* Parallax scroll image */}
      <Row className="mx-auto">
        <ParallaxBanner style={{height: '380px'}} layers={[
          {
            image: '/images/multiplex_overlay.webp',
            amount: 1
          }
        ]} />
      </Row>

      {/* Last Section */}
      <Row className="mx-auto pt-3 pb-5 mb-3 w-75">

        <Col xs={12} className="text-center py-4">
          <h1>Contribute Data</h1>
          <p className="small">Expand DeepCell Datasets by uploading new images.</p>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2 w-100">
          <Link to={Constants.SignUp}>
            <Button block variant="dark">
              Create an Account
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2 w-100">
          <Link to={Constants.SignIn}>
            <Button block variant="dark">
              Login
            </Button>
          </Link>
        </Col>

        <Col xs={12} md={4} className="text-center mb-2 w-100">
          <Button block variant="dark" href="https://deepcell.org/about">
            Learn More
          </Button>
        </Col>

      </Row>

    </Container>
  );
}
