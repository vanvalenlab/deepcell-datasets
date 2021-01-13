
import { lazy } from 'react';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import AllDatasets from './AllDatasets';

const DataCard = lazy(() => import('./DataCard'));

export default function Data() {

  return (
    <Container>

      <Row className="text-center py-4">
        <Col xs={12}>
          <h1>Curated Datasets</h1>
        </Col>
      </Row>

      <Row>
        {AllDatasets.map(d => {
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
