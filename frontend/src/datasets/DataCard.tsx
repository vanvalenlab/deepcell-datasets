import { useState } from 'react';
import { Storage } from '@aws-amplify/storage';
import { Dataset } from './AllDatasets';
import {
  Alert,
  Button,
  Card,
  ListGroup,
  ListGroupItem,
  Container,
  Dropdown,
  Row,
} from 'react-bootstrap';

const openInNewTab = (url: string) => {
  const newWindow = window.open(url, '_blank', 'noopener,noreferrer');
  if (newWindow) newWindow.opener = null;
};

type DataCardProps = {
  dataset: Dataset;
};

export default function DataCard({ dataset }: DataCardProps) {
  const [error, setError] = useState<string | null>(null);
  const { title, samples, imagingPlatform, thumbnail, versions } = dataset;
  const [version, setVersion] = useState(versions[0]);
  const { version: versionNumber, description, objectKey } = version;

  const onClick = async () => {
    try {
      const url = await Storage.get(objectKey, {
        expires: 60,
        customPrefix: {
          public: '',
        },
      });
      openInNewTab(url.toString());
    } catch (err) {
      setError(JSON.stringify(err));
    }
  };

  return (
    <Card>
      <Card.Img variant='top' src={thumbnail} />
      <Card.Body>
        <Card.Title className='mb-0'>{title}</Card.Title>
        <ListGroup variant='flush'>
          <ListGroupItem className='px-0 my-0'>
            <Card.Text>
              <strong>Imaging Platform:</strong> {imagingPlatform}
            </Card.Text>
          </ListGroupItem>
          <ListGroupItem className='px-0 my-0'>
            <Card.Text>
              <strong>Samples:</strong> {samples}
            </Card.Text>
          </ListGroupItem>
          <ListGroupItem className='px-0 my-0'>
            <Card.Text>
              <strong>Description:</strong> {description}
            </Card.Text>
          </ListGroupItem>
        </ListGroup>
        <Container>
          <Row className='justify-content-between'>
            <Dropdown>
              <Dropdown.Toggle variant='dark' id='dropdown-basic'>
                Version: {versionNumber}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                {versions.map((v) => (
                  <Dropdown.Item key={v.version} onClick={() => setVersion(v)}>
                    {v.version}
                  </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
            <Button variant='dark' onClick={onClick}>
              Download
            </Button>
          </Row>
        </Container>
        {error !== null ? (
          <Alert variant='danger' dismissible onClose={() => setError(null)}>
            {error}
          </Alert>
        ) : null}
      </Card.Body>
    </Card>
  );
}
