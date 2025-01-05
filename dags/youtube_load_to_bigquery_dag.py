from datetime import datetime, timedelta
from google.cloud import bigquery
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 9, 6, 0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG for loading data from GCS to BigQuery
dag = DAG(
    'youtube_load_to_bigquery',
    default_args=default_args,
    description='Load transformed JSON data from GCS to BigQuery',
    schedule_interval='*/20 * * * *',  # Runs every 20 minutes
    catchup=False,
)

def load_data_to_bigquery(bucket_name, dataset_name, table_name):
    # Initialize BigQuery client
    client = bigquery.Client()

    # Set GCS file path to load files from 'data/' directory
    gcs_file_path = f"gs://{bucket_name}/data/*.json"

    # Define the BigQuery table ID
    table_id = f"{client.project}.{dataset_name}.{table_name}"

        # Define schema to ensure consistency (matching your given schema)
    schema = [
        bigquery.SchemaField("title", "STRING"),
        bigquery.SchemaField("video_id", "STRING"),
        bigquery.SchemaField("channel_id", "STRING"),
        bigquery.SchemaField("channel_title", "STRING"),
        bigquery.SchemaField("category", "STRING"),
        bigquery.SchemaField("total_views", "INTEGER"),
        bigquery.SchemaField("likes", "INTEGER"),
        bigquery.SchemaField("dislikes", "INTEGER"),
        bigquery.SchemaField("comments", "INTEGER"),
        bigquery.SchemaField("publish_time", "TIMESTAMP"),
        bigquery.SchemaField("subscription_name", "STRING"),
        bigquery.SchemaField("message_id", "STRING"),
    ]

    # Configure load job
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        max_bad_records=10  # Allow up to 10 bad records to avoid minor issues blocking the load
    )

    # Load job
    load_job = client.load_table_from_uri(
        gcs_file_path,
        table_id,
        job_config=job_config,
    )

    # Wait for load job to complete
    load_job.result()

    # Get the destination table details
    destination_table = client.get_table(table_id)
    print(f"Loaded {destination_table.num_rows} rows into {dataset_name}.{table_name}")

# Define the PythonOperator task
load_task = PythonOperator(
    task_id='load_to_bigquery',
    python_callable=load_data_to_bigquery,
    op_kwargs={
        'bucket_name': 'us-central1-youtubepipeline-0006d8b4-bucket',
        'dataset_name': 'youtube_data',  # Replace with your BigQuery dataset name
        'table_name': 'raw_data'         # Replace with your BigQuery table name
    },
    dag=dag,
)

load_task
