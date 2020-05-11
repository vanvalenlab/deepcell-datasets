FROM python:3.7

# System maintenance
RUN apt-get update && apt-get install -y \
        git \
        python3-tk \
        libsm6 && \
    rm -rf /var/lib/apt/lists/* && \
    /usr/local/bin/pip install --upgrade pip

WORKDIR /notebooks

# Copy the requirements.txt and install the dependencies
COPY setup.py requirements.txt /opt/deepcell-datasets/
RUN pip install -r /opt/deepcell-datasets/requirements.txt

# Copy the rest of the package code and its scripts
COPY deepcell_datasets /opt/deepcell-datasets/deepcell_datasets

# Install deepcell_datasets via setup.py
RUN pip install /opt/deepcell-datasets

# Copy over toolbox notebooks
COPY notebooks/ /notebooks/

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
