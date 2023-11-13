from distutils.core import setup, find_packages

setup(
    name='kbc_transformation',
    version='1.0',
    url='https://github.com/keboola/python-transformation-v2',
    packages=find_packages(exclude=['tests']),
    requires=['pip']
)
