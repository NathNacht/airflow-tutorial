import textwrap
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.base import BaseSensorOperator
from datetime import datetime, timedelta

import os

class FileSensor(BaseSensorOperator):
    def __init__(self, file_path, retries, retry_delay, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_path = file_path
        self.retries = retries
        self.retry_delay = retry_delay

    def poke(self, context):
        if os.path.exists(self.file_path):
            return True
        return False

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email' : ['datanerd07@gmail.com'],
    'email_on_failure': True
}

with DAG(
    dag_id='dag_clean_train',
    default_args=default_args,
    description='Clean and train a model on immo data',
    start_date=datetime(2024, 5, 2, 2),
    schedule_interval='@daily'
) as dag:
    
    file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    file_path='/opt/airflow/project/data/raw/raw_huis_te_koop.csv',
    mode='poke',
    retries=3,
    dag=dag
    )

    file_sensor_task.doc_md = textwrap.dedent(
        """\
    #### Task Documentation
    This task looks for the existence of the raw_huis_te_koop.csv file in the data/raw folder.    
    """
    )

    cleantask = BashOperator(
    task_id='cleaningtask',
    bash_command='python /opt/airflow/project/immo-eliza-2cleaning/clean.py',
    dag=dag,
    )

    cleantask.doc_md = textwrap.dedent(
    """
    #### Task Documentation
    This task cleans the raw CSVs of both houses and apartments and stores a clean version in the `data/cleaned` folder.
    
    **Steps taken at cleaning:**
    - Stripping blanks from all columns
    - Removing duplicates based on `property_id`
    - Removing records with empty `price` field
    - Removing records with empty `area` field
    - Removing records with empty `living area`
    - Removing street names and house numbers
    - Removing empty records that only have `property_id`
    - Removing houses in apartments and apartments in houses
    - Lowercasing all locality names
    - Removing houses and apartments that are not in Belgium
    - Translating the locality names to Dutch
    - Adding province names to the records
    """
    )
    
    notify_cleaned = BashOperator(
    task_id="notify_cleaned",
    bash_command='echo "raw data cleaning done"',
    dag=dag,
    )

    modeltraintask = BashOperator(
    task_id='modeltrainingtask',
    bash_command='python /opt/airflow/project/immo-eliza-model/train_with_pipeline.py',
    dag=dag,
    )

    modeltraintask.doc_md = textwrap.dedent(
    """
    #### Task Documentation
    This modeltraining uses randomforestregressor with cross validation.
    Models are saved in the `data/models` folder.
    """
    )

    notify_trained = BashOperator(
    task_id="notify_trained",
    bash_command='echo "training data done"',
    dag=dag,
    )

    file_sensor_task >> cleantask >> notify_cleaned >> modeltraintask >> notify_trained