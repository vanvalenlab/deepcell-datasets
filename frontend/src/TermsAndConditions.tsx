import React from 'react';
import Container from 'react-bootstrap/Container';
import  styled  from  'styled-components';

const CircleBullet = styled.li`
  list-style-type: circle !important;
`;

export default function TermsAndConditions() {
  return (
    <Container className="text-center mx-auto">
      <h1>Terms & Conditions</h1>

      <p>By using this site you (the "Researcher") acknowledge that:</p>

        <ul>

          <CircleBullet>Researcher shall use any data obtained here only for non-commercial research and educational purposes.</CircleBullet>

          <CircleBullet>Researcher retains permission to perform analysis on any raw images provided.</CircleBullet>

          <CircleBullet>Researcher gives the owner of this site unrestricted permission to use any submitted images for any purpose with or without attribution.</CircleBullet>

          <CircleBullet>Use of any images from this site used in research or publications must be accredited.</CircleBullet>

          <CircleBullet>All data made available by this site is licensed under the following <a href="https://github.com/vanvalenlab/deepcell-datasets/blob/master/LICENSE">license</a>.</CircleBullet>

        </ul>
    </Container>
  );
}
