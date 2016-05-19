#FROM ubuntu:16.04
FROM nginx:1.10

MAINTAINER Nikolay Telepenin <ntelepenin@cloudlinux.com>

ENV DEBIAN_FRONTEND=noninteractive VENV_PATH=/root/venv

RUN apt-get update && apt-get install -y wget
RUN wget https://dl.eff.org/certbot-auto && chmod a+x ./certbot-auto
RUN ln -s certbot-auto letsencrypt-auto
RUN ./letsencrypt-auto --help all


RUN apt-get install -y python-bottle
#ADD bottle.ini /etc/uwsgi/apps-available/bottle.ini
#RUN ln -s /etc/uwsgi/apps-available/bottle.ini /etc/uwsgi/apps-enabled/bottle.ini
#RUN apt-get install -y supervisor

#ADD bottle.conf /etc/nginx/conf.d/bottle.conf
ADD app.py /opt/certbot/app.py
#RUN rm -rf /var/lib/apt/lists/*
#RUN rm /etc/nginx/conf.d/default.conf

#ADD supervisor-app.conf  /etc/supervisor/conf.d/supervisor-app.conf


VOLUME /etc/letsencrypt /var/lib/letsencrypt

WORKDIR /opt/certbot
#CMD ["nginx", "-g", "daemon off;"]
#CMD ["supervisord", "-n"]
CMD ["python", "app.py", "80"]