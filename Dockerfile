FROM python:3.7

WORKDIR /usr/src/app

# Copy the requirements.txt and install the dependencies
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the package code and its scripts
COPY . .

EXPOSE 5000

CMD ["/bin/sh", "-c", "python application.py"]
