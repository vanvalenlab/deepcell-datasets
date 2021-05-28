/**
 * For the POC the "data" will just be hard coded.
 * 
 * The next step would be to load this from a Data API
 * Hopefully a Lambda+DynamoDB serverless API!
 */

const AllDatasets = [
  {
    title: 'TissueNet Version 1.0',
    objectKey: 'tissuenet/tissuenet_v1.0.zip',
    thumbnail: '/images/multiplex_overlay.webp',
    imagingPlatform: 'Multiplexed imaging',
    samples: '2D tissue',
    description: 'This is the first release of the TissueNet dataset from Greenwald, Miller et al.',
  }
];

export default AllDatasets;
