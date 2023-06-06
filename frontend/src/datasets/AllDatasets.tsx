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
    title: 'DynamicNuclearNet Segmentation',
    thumbnail: '/images/3t3_nuclear_outlines.webp',
    imagingPlatform: 'Fluorescent Microscopy',
    samples: '2D cell culture',
    versions: [
      {
        version: '1.0',
        description: 'This is the first release of the DynamicNuclearNet segmentation dataset from Schwartz et al. 2023',
        objectKey: 'dynamic_nuclear_net/DynamicNuclearNet-segmentation-v1_0.zip',
      },
    ],
  },
  {
    title: 'DynamicNuclearNet Tracking',
    thumbnail: '/images/3t3_nuclear_outlines.webp',
    imagingPlatform: 'Fluorescent Microscopy',
    samples: '2D cell culture',
    versions: [
      {
        version: '1.0',
        description: 'This is the first release of the DynamicNuclearNet tracking dataset from Schwartz et al. 2023',
        objectKey: 'dynamic_nuclear_net/DynamicNuclearNet-tracking-v1_0.zip',
      },
    ],
  },
];

export default AllDatasets;
