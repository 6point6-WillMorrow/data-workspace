# Analysis Workspace [![CircleCI](https://circleci.com/gh/uktrade/analysis-workspace.svg?style=svg)](https://circleci.com/gh/uktrade/analysis-workspace)

Allows users to launch applications in order to analyse data


## Running locally

Set the required variables by

```bash
cp example.env .env
```

and edit `.env`, specifically replacing `AUTHBROKER_*`. Start the application by

```bash
docker-compose up --build
```

With the default environment, you will need the below in your `/etc/hosts` file.

```
127.0.0.1       localapps.com
```

And the application will be visible at http://localapps.com. This is to be able to properly test cookies that are shared with subdomains.


## Creating migrations / running management commands

```bash
docker-compose build && \
docker-compose run \
    --user root \
    --volume=$PWD/app/app/migrations:/app/app/migrations \
    analysis-workspace django-admin makemigrations
```

For other commands, replace `makemigrations` with the name of the command.


## Running tests

```bash
docker-compose build analysis-workspace && \
docker-compose -f docker-compose-test.yml build && \
docker-compose -f docker-compose-test.yml run analysis-workspace-test python3 -m unittest test.test
```


# Building & pushing docker image to Quay.io

```bash
docker build -t analysis-workspace . && \
docker tag analysis-workspace:latest quay.io/uktrade/jupyterhub-data-auth-admin:latest && \
docker push quay.io/uktrade/jupyterhub-data-auth-admin:latest
```


## Healthcheck

```bash
docker build -t data-workspace-healthcheck . -f Dockerfile-healthcheck && \
docker tag data-workspace-healthcheck:latest quay.io/uktrade/data-workspace-healthcheck:latest && \
docker push quay.io/uktrade/data-workspace-healthcheck:latest
```

Quay.io does not build the images: they are built locally and pushed.
