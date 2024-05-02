from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='dag_1clean',
    default_args=default_args,
    description='Clean immo data',
    start_date=datetime(2024, 4, 30, 2),
    schedule_interval='@daily'
) as dag:
    
    # file_sensor_task = FileSensor(
    # task_id='file_sensor_task',
    # filepath='/opt/airflow/plugins/data/raw/raw_huis_te_koop.csv',
    # dag=dag
    # )

    cleantask = BashOperator(
    task_id='cleaningtask',
    bash_command='python /opt/airflow/plugins/immo-eliza-2cleaning/clean.py',
    schedule_interval=None,
    dag=dag,
    )
    
    notify = BashOperator(
    task_id="notify",
    bash_command='echo "raw data cleaning done"',
    dag=dag,
    )

    # file_sensor_task >> 
    cleantask >> notify
