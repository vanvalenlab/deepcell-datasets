import { Link } from '@reach/router';
import React from 'react';
import  styled  from  'styled-components';

import Constants from './Constants';

const StyledFooter = styled.footer`
  flex: none;
`;

export default class Footer extends React.Component {
  render() {
    const fullDate = new Date();
    const year = fullDate.getFullYear();

    return (
      <StyledFooter className='mt-auto py-3 bg-dark text-center'>

        <div className='text-secondary small'>
          © 2016-{year} The Van Valen Lab at the California Institute of Technology
          (Caltech). All rights reserved. <Link to={Constants.Privacy}>Privacy Policy</Link> & <Link to={Constants.Terms}>Terms & Conditions</Link>.
        </div>

      </StyledFooter>
    );  
  }
}