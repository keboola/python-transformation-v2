[![Build Status](https://dev.azure.com/keboola-dev/Data%20Science/_apis/build/status/keboola.python-transformation-v2?branchName=refs%2Ftags%2F0.3.3)](https://dev.azure.com/keboola-dev/Data%20Science/_build/latest?definitionId=74&branchName=refs%2Ftags%2F0.3.3)

Application which runs KBC transformations writen in Python, interface is provided by [docker-bundle](https://github.com/keboola/docker-bundle).

### Installation
Package is available only on Github, so you need to use `pip` to install the package
```
pip install --upgrade git+git://github.com/keboola/python-transformation-v2.git
```

### Dev
- clone the repo
- `export BASE_IMAGE=quay.io/keboola/docker-custom-python:latest` or provide the tag you want, say `2.2.0`
- `./create_dockerfile.sh`
- `docker-compose build`

### Run tests
- `docker-compose run --rm python-transformation-v2`
