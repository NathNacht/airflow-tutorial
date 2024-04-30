# Immo Eliza with Airflow
[![Airflow](https://img.shields.io/badge/Airflow-2.9.0-blue)](https://airflow.apache.org/)

## Info

This airflow pipeline combines the code from previous projects on immo eliza.
Instead of having all the code in different repo's, it runs the code in different steps.

The projects consisted out of:

1. scraping immoweb
2. cleaning data
3. creating a model
4. training the model
5. deploying the model

# Airflow Information

Adding some more information on airflow as this project was a good introduction into working with Airflow

### Sources

https://www.youtube.com/watch?v=Sva8rDtlWi4 to have a first working Airflow version

### Prerequisites:
- have docker installed
- have docker compose installed

### Steps followed

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

Creation of an .env file with the AIRFLOW_UID = 1000. This is the user id of the host user (to be found in /etc/passwd). We need to place it here so our user has root permissions to run and trigger commands (when working with docker-compose)

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



