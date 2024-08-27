from setuptools import setup

setup(
    name='kbc_transformation',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    url='https://github.com/keboola/python-transformation-v2',
    packages=['kbc_transformation'],
    requires=['pip'],
    install_requires=['keboola.component'],
    license="MIT"
)
