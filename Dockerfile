# Grab the docker python image
FROM ghcr.io/opensafely-core/python:latest as base-python

# Upgrade pip and safetab
RUN python -m pip install -U pip setuptools wheel && \
    python -m pip install safetab-action

# point to right file
CMD python entrypoint.py

# define entry point
ENTRYPOINT ["safetab"]