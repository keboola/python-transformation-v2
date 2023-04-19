ARG BASE_IMAGE_NAME
ARG BASE_IMAGE_TAG
FROM ${BASE_IMAGE_NAME}:${BASE_IMAGE_TAG}

# Create directory for user packages
# This directory is usually created automatically by pip
# ... but if it doesn't exist when you run the script
# ... then the modules installed during the transformation are not loaded automatically!
# ... because the loader thinks that this directory does not exist (it did not exist at the start of the script)
# Eg. mkdir -p /var/www/.local/lib/python3.8/site-packages
RUN . "$VIRTUAL_ENV/bin/activate" && mkdir -p $(su www-data -s /bin/bash -c "python -c 'import site; print(site.USER_SITE)'")

# Make home directory writable
RUN chown -R www-data:www-data /var/www

WORKDIR /code/

COPY ./src ./src
COPY ./tests ./tests
COPY main.py README.md ./

RUN . "$VIRTUAL_ENV/bin/activate" && pip freeze

CMD . "$VIRTUAL_ENV/bin/activate" && python -X faulthandler -u /code/main.py
