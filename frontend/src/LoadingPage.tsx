import { Container, Spinner } from 'react-bootstrap';

export default function LoadingPage() {
  return (
    <Container className="mx-auto text-center">
      <Spinner animation="border" variant="dark" />
    </Container>
  );
};
