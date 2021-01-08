import { Button, Nav, Navbar } from 'react-bootstrap';
import { FaSignInAlt, FaPlusSquare, FaSignOutAlt } from 'react-icons/fa';
// import Form from 'react-bootstrap/Form';
// import FormControl from 'react-bootstrap/FormControl';
import Constants from './Constants';

// https://react-bootstrap.github.io/components/navbar/

export default function NavigationToolbar(props: any) {

  const isLoggedIn = props.isLoggedIn || false;

  return (
    <Navbar variant="dark" bg="dark" expand="md" sticky="top">
      <Navbar.Brand href="/">DeepCell Datasets</Navbar.Brand>
      <Navbar.Toggle aria-controls="navbar-nav" />
      <Navbar.Collapse id="navbar-nav">
        {/* <Form inline>
          <FormControl type="text" placeholder="SearchName" className="mr-sm-2"  size="sm" />
          <Button variant="outline-light" size="sm">Search</Button>
        </Form> */}
        
        { isLoggedIn ?
          <Nav className="ml-auto">
            <Nav.Link href={Constants.SignOut}>
              <Button variant="outline-light" size="sm">
                <FaSignOutAlt /> Logout
              </Button>
            </Nav.Link>
          </Nav>
          :
          <Nav className="ml-auto">
            <Nav.Link href={Constants.SignUp}>
              <Button variant="outline-light" size="sm">
                <FaPlusSquare /> Sign Up
              </Button>
            </Nav.Link>
            <Nav.Link href={Constants.SignIn}>
              <Button variant="outline-light" size="sm">
                <FaSignInAlt /> Login
              </Button>
            </Nav.Link>
          </Nav>
        }
      </Navbar.Collapse>
    </Navbar>
  );
}
