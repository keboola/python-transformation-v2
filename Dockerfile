FROM quay.io/keboola/docker-custom-python:2.0.4

COPY . /code/
WORKDIR /code/
CMD ["python", "-u", "/code/main.py"]
