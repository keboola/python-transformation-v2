[![Build Status](https://dev.azure.com/keboola-dev/Data%20Science/_apis/build/status/keboola.python-transformation-v2?branchName=master)](https://dev.azure.com/keboola-dev/Data%20Science/_build/latest?definitionId=74&branchName=master)

This application runs Keboola transformations writen in Python. The interface is provided by [docker-bundle](https://github.com/keboola/docker-bundle).

### Installation
The package is available only on GitHub. You must use `pip` to install the package.
```
pip install --upgrade git+git://github.com/keboola/python-transformation-v2.git
```

### Development
- Clone the repository.
- Build the Docker image: 
  </br>`docker compose build --build-arg BASE_IMAGE_TAG=python-3.8-6.0.0 python-transformation-v2` (or provide the tag you want)
- Initialize the PyPi mirror:
</br> `docker compose run --rm bandersnatch bandersnatch mirror`

### Run Tests
Run the tests using the following command:

`docker compose run --rm python-transformation-v2`
