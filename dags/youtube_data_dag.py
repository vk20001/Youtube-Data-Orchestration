from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import sys

# Add path for fetch.py if needed
fetch_script_path = os.path.dirname(os.path.realpath(__file__))
if fetch_script_path not in sys.path:
    sys.path.insert(0, fetch_script_path)

# Import the function from fetch.py
from fetch import fetch_data

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 9, 4, 30),  # Set this to a recent time (UTC)
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'youtube_data_pipeline',
    default_args=default_args,
    description='Fetch YouTube data and publish to Pub/Sub',
    schedule_interval='*/10 * * * *',  # Schedule to run every 10 minutes
    catchup=False,
)

# Define the PythonOperator task to run fetch.py
fetch_task = PythonOperator(
    task_id='fetch_youtube_data',
    python_callable=fetch_data,
    dag=dag,
)

fetch_task
