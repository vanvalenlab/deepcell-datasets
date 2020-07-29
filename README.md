# DeepCell Datasets: Master Data Management for DeepCell

[![Actions Status](https://github.com/vanvalenlab/deepcell-datasets/workflows/Test%20API/badge.svg)](https://github.com/vanvalenlab/deepcell-datasets/actions)
[![Coverage Status](https://coveralls.io/repos/github/vanvalenlab/deepcell-datasets/badge.svg?branch=master)](https://coveralls.io/github/vanvalenlab/deepcell-datasets?branch=master)

DeepCell Datasets is a collection of data engineering and versioning tools for the management of optical microscopy images and its associated metadata. This Master Data Management allows for a single entry point for access to the lab's raw data and provides to means to pair them with crowdsourced annotations to create custom training data for [DeepCell](https://github.com/vanvalenlab/deepcell-tf).

## Getting Started

DeepCell Datasets uses `nvidia-docker` and `mongodb` to keep track of new images. A Flask API provides convenient access to the database.

## Copyright

Copyright © 2016-2020 [The Van Valen Lab](http://www.vanvalen.caltech.edu/) at the California Institute of Technology (Caltech), with support from the Paul Allen Family Foundation, Google, & National Institutes of Health (NIH) under Grant U24CA224309-01.
All rights reserved.

## License

This software is licensed under a modified [APACHE2](LICENSE).

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

See [LICENSE](LICENSE) for full details.

## Trademarks

All other trademarks referenced herein are the property of their respective owners.

## Credits

[![Van Valen Lab, Caltech](https://upload.wikimedia.org/wikipedia/commons/7/75/Caltech_Logo.svg)](http://www.vanvalen.caltech.edu/)
