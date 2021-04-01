/**
 * For the POC the "data" will just be hard coded.
 * 
 * The next step would be to load this from a Data API
 * Hopefully a Lambda+DynamoDB serverless API!
 */

const AllDatasets = [
  // {
  //   title: 'TissueNet Multiplex',
  //   object_key: 'multiplex/20201018_multiplex_seed_0.zip',
  //   thumbnail: '/images/multiplex_overlay.webp',
  //   text: 'Multiplex tissue images from a variety of platforms (MIBI, Vectra, etc.)',
  // },
  {
    title: 'TissueNet Multiplex (Test Set)',
    object_key: 'multiplex/20201018_multiplex_seed_0_test_256x256.npz',
    thumbnail: '/images/multiplex_overlay.webp',
    text: 'Multiplex tissue images from a variety of platforms (MIBI, Vectra, etc.)',
  }
];

export default AllDatasets;
