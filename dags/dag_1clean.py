from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
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
    cleantask = BashOperator(
    task_id='cleaningtask',
    bash_command='python /opt/airflow/plugins/immo-eliza-2cleaning/clean.py',
    dag=dag,
)
    
    cleantask
