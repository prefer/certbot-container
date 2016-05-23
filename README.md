# Container with 

## Prerequisites
* Docker 1.10 or higher

## Install 

```
$ git clone https://github.com/prefer/certbot-container.git
$ cd certbot-container
```

## Build

```
$ export CERTBOT_IMAGE="prefer/certbot:0.36" 
$ docker build -t $CERTBOT_IMAGE .
$ docker push $CERTBOT_IMAGE
```

## Run

```
$ docker run -d -p 8001:80 prefer/certbot:0.36
```