# Grab the docker python image
FROM ghcr.io/opensafely-core/python:latest as base-python

# Upgrade pip and safetab
RUN python -m pip install -U pip setuptools wheel && \
    python -m pip install safetab-action

# labeling
LABEL org.opencontainers.image.title="safetab" \
      org.opencontainers.image.description="Safetab action for opensafely.org" \
      org.opencontainers.image.source="https://github.com/opensafely-core/safetab-action" \
      org.opensafely.action="safetab"

# re-use entrypoint from base-docker image
ENV ACTION_EXEC=safetab

