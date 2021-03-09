import Container from 'react-bootstrap/Container';
import Spinner from 'react-bootstrap/Spinner';

export default function LoadingPage() {
  return (
    <Container className="mx-auto text-center">
      <Spinner animation="border" variant="dark" />
    </Container>
  );
};
