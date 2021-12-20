# DeepCell Datasets

[![Actions Status](https://github.com/vanvalenlab/deepcell-datasets/workflows/Test%20API/badge.svg)](https://github.com/vanvalenlab/deepcell-datasets/actions)
[![Coverage Status](https://coveralls.io/repos/github/vanvalenlab/deepcell-datasets/badge.svg?branch=master)](https://coveralls.io/github/vanvalenlab/deepcell-datasets?branch=master)

## Getting Started

DeepCell Datasets is a serverless applicatioin that allows authenticated users to access published datasets.
This is aided by using `lectra` as well as the `serverless` framework.
`lerna` enables us to easily control all of the services from the root directory, while `serverless` allows us to deploy and manage AWS infrastructure through `.yml` configuration files.

### Deployment

`lectra` is used to manage and deploy both the frontend and the application services with a simple `yarn` or `npm` command:

```bash
yarn deploy:dev
# yarn deploy:prod
```

### Architecture

The application implements a microservice architecture made up of the following components:

- [`frontend`](frontend/): a static webpage that is the primary interface of the application.
- [AWS Congito](https://aws.amazon.com/cognito): An AWS service that handles all user authentication. Users that have confirmed their email address are authenticated to download data in a protected S3 bucket. The authentication React components have been overridden in `frontend/src/auth` to provide the application with a cohesive style.
- [`send-email`](services/send-email): an AWS Lambda service that can send email to admins on behalf of new users.
- [`validate-email-domain`](services/validate-email-domain): a deprecated service that whitelists certain domains for account creation. This is used as a pre-signup hook for AWS Cognito.

### How to update with new data

Data is saved in a protected S3 bucket, but to enable users to view and download these datasets, the details must be saved in [`frontend/src/datasets/AllDatasets.tsx`](frontend/src/datasets/AllDatasets.tsx).

This is a simple JSON object that has the following fields:

| Name | Description |
| :--- | :--- |
| `title` | The name of the dataset. |
| `objectKey` | The path to the dataset inside the S3 bucket. |
| `thumbnail` | The path to the thumbnail example, which must be saved in `frontend/public/images`. |
| `imagingPlatform` | The imaging platform that created the dataset. |
| `samples` | The type of image data. |
| `description` | A brief description of the data. |

## Copyright

Copyright © 2016-2021 [The Van Valen Lab](http://www.vanvalen.caltech.edu/) at the California Institute of Technology (Caltech), with support from the Paul Allen Family Foundation, Google, & National Institutes of Health (NIH) under Grant U24CA224309-01.
All rights reserved.

## License

This software is licensed under a modified [APACHE2](LICENSE).

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

See [LICENSE](LICENSE) for full details.

## Trademarks

All other trademarks referenced herein are the property of their respective owners.

## Credits

[![Van Valen Lab, Caltech](https://upload.wikimedia.org/wikipedia/commons/7/75/Caltech_Logo.svg)](http://www.vanvalen.caltech.edu/)
