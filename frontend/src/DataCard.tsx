import { useState } from 'react';
import { Storage } from '@aws-amplify/storage';
import Alert from 'react-bootstrap/Alert';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

const openInNewTab = (url: string) => {
  const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
  if (newWindow) newWindow.opener = null
}

export default function DataCard (props: any) {
  const [error, setError] = useState<string|null>(null);
  const title = props.title || 'Data Title';
  const text = props.text || 'Data description';
  const thumbnail = props.thumbnail || '';
  const objectKey = props.objectKey || '';

  const onClick = async () => {
    try {
      const url = await Storage.get(objectKey, {
        expires: 60,
        customPrefix: {
          public:''
        }
      });
      openInNewTab(url.toString());
    } catch (err) {
      setError(JSON.stringify(err));
    }
  }

  return (
    <Card>
      <Card.Img variant="top" src={thumbnail} />
      <Card.Body>
        <Card.Title>{title}</Card.Title>
        <Card.Text>{text}</Card.Text>
        <Button variant="dark" onClick={onClick}>Download</Button>
        { (error !== null) ?
          <Alert variant="danger" dismissible onClose={() => setError(null)}>
            {error}
          </Alert>
          : null
        }
      </Card.Body>
    </Card>
  );
};
