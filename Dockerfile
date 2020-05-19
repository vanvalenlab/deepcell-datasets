FROM python:3.7

# System maintenance
RUN apt-get update && apt-get install -y \
        git \
        python3-tk \
        libsm6 && \
    rm -rf /var/lib/apt/lists/* && \
    /usr/local/bin/pip install --upgrade pip

WORKDIR /usr/src/app

# Copy the requirements.txt and install the dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the package code and its scripts
COPY . .

EXPOSE 5000

CMD ["/bin/sh", "-c", "python application.py"]
