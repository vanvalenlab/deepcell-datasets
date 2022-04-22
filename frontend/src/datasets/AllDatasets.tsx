/**
 * For the proof of concept the "data" will just be hard coded.
 *
 * The next step would be to load this from a Data API
 * Hopefully a Lambda+DynamoDB serverless API!
 */

interface Version {
  version: string;
  description: string;
  objectKey: string;
}

export interface Dataset {
  title: string;
  samples: string;
  imagingPlatform: string;
  thumbnail: string;
  versions: Version[];
}

const AllDatasets: Dataset[] = [
  {
    title: 'TissueNet',
    thumbnail: '/images/multiplex_overlay.webp',
    imagingPlatform: 'Multiplexed imaging',
    samples: '2D tissue',
    versions: [
      {
        version: '1.0',
        description:
          'This is the first release of the TissueNet dataset from Greenwald, Miller et al.',
        objectKey: 'tissuenet/tissuenet_v1.0.zip',
      },
      {
        version: '1.1',
        description:
          'This is the second release of the TissueNet dataset from Greenwald, Miller et al.',
        objectKey: 'tissuenet/tissuenet_v1.1.zip',
      },
    ],
  },
  {
    title: 'LiveCellNet',
    thumbnail: '/images/3t3_nuclear_outlines.webp',
    imagingPlatform: 'Fluorescent Microscopy',
    samples: '2D culture',
    versions: [
      {
        version: '0.1',
        description: 'This is a subset of the Nuclear Tracking dataset.',
        objectKey: 'tracking-nuclear/val.trks',
      },
    ],
  },
];

export default AllDatasets;
