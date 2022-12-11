FROM --platform=linux/amd64 python:3.7.15-slim

RUN --mount=type=secret,id=USERNAME \
    --mount=type=secret,id=PASSWORD \
    export USERNAME=$(cat /run/secrets/USERNAME) && \
    export PASSWORD=$(cat /run/secrets/PASSWORD)

ARG USERNAME
ARG PASSWORD

ENV USERNAME_ENV=$USERNAME
ENV PASSWORD_ENV=$PASSWORD

RUN pip3 install --extra-index-url https://$USERNAME_ENV:$PASSWORD_ENV@pypi.netsquid.org netsquid
RUN pip3 install matplotlib
