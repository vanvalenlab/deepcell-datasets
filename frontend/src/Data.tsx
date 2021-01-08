import { useState } from 'react';
import { Storage } from '@aws-amplify/storage';
import { Alert, Button, Card, Col, Container, Row } from 'react-bootstrap';
import TissueNetThumbnail from './images/multiplex_overlay.png';

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
    thumbnail: TissueNetThumbnail,
    text: 'Multiplex tissue images from a variety of platforms (MIBI, Vectra, etc.)',
  }
];

export default function Data() {
  const [error, setError] = useState<string|null>(null);

  const DataCard = (props: any) => {
    const title = props.title || "Data Title";
    const text = props.text || "Data description";
    const thumbnail = props.thumbnail || TissueNetThumbnail;
    const objectKey = props.objectKey || '';

    const openInNewTab = (url) => {
      const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
      if (newWindow) newWindow.opener = null
    }
 
    const onClick = async () => {
      try {
        const url = await Storage.get(objectKey, {
          expires: 60,
          customPrefix: {
            public:''
          }
        });
        console.log(url);
        openInNewTab(url);
      } catch (err) {
        setError(JSON.stringify(err));
      }
    }

    return (
      <Card style={{ width: '18rem' }}>
        <Card.Img variant="top" src={thumbnail} />
        <Card.Body>
          <Card.Title>{title}</Card.Title>
          <Card.Text>{text}</Card.Text>
          <Button variant="dark" onClick={onClick}>Download</Button>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Container fluid>

      <Row className="text-center py-4">
        <Col xs={12}>
          <h1>Curated Datasets</h1>
        </Col>
      </Row>

      { (error !== null) ?
        <Alert variant="danger" dismissible onClose={() => setError(null)}>
          {error}
        </Alert>
        : null
      }

      <Container>
        <Row>
          {allData.map(d => {
            return (
              <Col xs={12} md={4} key={d.object_key} className="mx-auto mb-4">
                <DataCard title={d.title} objectKey={d.object_key} text={d.text} />
              </Col>
            );
          })}
        </Row>
      </Container>

    </Container>
  );
}
