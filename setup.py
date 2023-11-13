from setuptools import setup, find_packages

setup(
    name='kbc_transformation',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='https://github.com/keboola/python-transformation-v2',
    packages=find_packages(exclude=['tests']),
    requires=['pip'],
    license="MIT"
)
