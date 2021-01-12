
import { lazy } from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

const DataCard = lazy(() => import('./DataCard'));

/**
 * For the POC the "data" will just be hard coded.
 * 
 * The next step would be to load this from a Data API
 * Hopefully a Lambda+DynamoDB serverless API!
 */
const allData = [
  {
    title: 'TissueNet Multiplex',
    object_key: 'multiplex/20201018_multiplex_seed_0.zip',
    thumbnail: '/images/multiplex_overlay.webp',
    text: 'Multiplex tissue images from a variety of platforms (MIBI, Vectra, etc.)',
  }
];

export default function Data() {

  return (
    <Container>

      <Row className="text-center py-4">
        <Col xs={12}>
          <h1>Curated Datasets</h1>
        </Col>
      </Row>

      <Row>
        {allData.map(d => {
          return (
            <Col xs={12} md={4} key={d.object_key} className="mx-auto mb-4">
              <DataCard title={d.title} objectKey={d.object_key} text={d.text} thumbnail={d.thumbnail} />
            </Col>
          );
        })}
      </Row>

    </Container>
  );
}
