# Airflow Tutorial

![Airflow](https://img.shields.io/badge/Airflow-2.9.0-blue)

## Introduction

Starting from https://www.youtube.com/watch?v=Sva8rDtlWi4 to have a working Airflow installation.

## Prerequisites:
- have docker installed
- have docker compose installed

## Steps followed

Airflow should NOT be installed locally!! This is done through the docker-compose file

1. From https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html fetched the docker-compose.yaml file

```	bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
```

This file contains several service definitions:

- airflow-scheduler - The scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
- airflow-webserver - The webserver is available at http://localhost:8080.
- airflow-worker - The worker that executes the tasks given by the scheduler.
- airflow-triggerer - The triggerer runs an event loop for deferrable tasks.
- airflow-init - The initialization service.
- postgres - The database.
- redis - The redis - broker that forwards messages from scheduler to worker.

2. Creation config, dags, logs and plugins folder and set AIRFLOW_UID

On Linux, the quick-start needs to know your host user id and needs to have group id set to 0. Otherwise the files created in dags, logs and plugins will be created with root user ownership. You have to make sure to configure them for the docker-compose

```	bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
# or
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

3. Running airflow-init

```	bash
docker compose up airflow-init
```

4. Starting the remaining services

```	bash
docker compose up
``` 

Airflow GUI is now available at: http://localhost:8080/


5. Tear down the environment

```	bash
docker compose down --volumes --remove-orphans
# or
docker compose down --volumes --rmi all
```

6. Troubleshooting

Logging in into a running container:

```	bash
docker compose exec airflow-worker /bin/bash
```

Connecting to the postgres database:

```	bash
docker compose exec postgres psql -U airflow -d airflow
```



