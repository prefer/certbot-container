FROM ubuntu:16.04

MAINTAINER Nikolay Telepenin <ntelepenin@cloudlinux.com>

ENV DEBIAN_FRONTEND=noninteractive VENV_PATH=/root/venv

WORKDIR /opt/certbot

RUN apt-get update && apt-get install -y wget
RUN wget https://dl.eff.org/certbot-auto && chmod a+x ./certbot-auto
RUN ln -s certbot-auto letsencrypt-auto
RUN ./letsencrypt-auto --help all

RUN apt-get install -y python3-pip && pip3 install aiohttp

VOLUME /etc/letsencrypt /var/lib/letsencrypt
COPY . /opt/certbot

CMD ["python3.5", "server.py", "80"]