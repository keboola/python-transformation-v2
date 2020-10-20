FROM quay.io/keboola/docker-custom-python:2.0.4

# Create director for user packages
# This directory is usually created automatically by pip
# ... but if it doesn't exist when you run the script
# ... then the modules installed during the transformation are not loaded automatically!
# ... because the loader thinks that this directory does not exist (it did not exist at the start of the script)
RUN mkdir -p /var/www/.local/lib/python3.8/site-packages

# Make home directory writable
RUN chown -R www-data:www-data /var/www

COPY . /code/
WORKDIR /code/
CMD ["python", "-u", "/code/main.py"]
