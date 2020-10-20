FROM quay.io/keboola/docker-custom-python:2.0.4

# Make home directory writable, so packages can be installed
RUN mkdir -p /var/www && chown www-data:www-data /var/www

COPY . /code/
WORKDIR /code/
CMD ["python", "-u", "/code/main.py"]
