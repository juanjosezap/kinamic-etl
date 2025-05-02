from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import os
import subprocess
import sys

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define another DAG with different schedule for a parameterized spider
with DAG(
    'scrapinghub_dag',
    default_args=default_args,
    description='A DAG to run the artworkspider',
    schedule_interval=timedelta(hours=2),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['scrapy'],
) as dag:
    
    # Run the spider using BashOperator as an alternative approach
    t1 = BashOperator(
        task_id='run_artworks_spider',
        bash_command='cd /opt/airflow/scrapinghub/ && '
                    'scrapy crawl artworkspider '
                    '-O /opt/airflow/scrapy_output/arworkspider_{{ ds }}_{{ execution_date.hour }}.json',
    )
    
    t1