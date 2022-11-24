FROM --platform=linux/amd64 python:3.7.15-slim

ARG USERNAME
ARG PASSWORD
ENV USERNAME_ENV=$USERNAME
ENV PASSWORD_ENV=$PASSWORD

RUN pip3 install --extra-index-url https://$USERNAME_ENV:$PASSWORD_ENV@pypi.netsquid.org netsquid
