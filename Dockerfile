FROM quay.io/keboola/docker-custom-python:2.0.4

RUN mkdir -p /var/www && chown www-data:www-data /var/www
COPY . /code/
WORKDIR /code/
CMD ["python", "-u", "/code/main.py"]
