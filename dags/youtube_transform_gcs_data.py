from datetime import datetime, timedelta
import json
from google.cloud import storage
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 9, 5, 0),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG for transforming GCS data
dag = DAG(
    'youtube_transform_gcs_data',
    default_args=default_args,
    description='Transform Pub/Sub GCS data to valid JSON files and save to data directory',
    schedule_interval='*/10 * * * *',  # Runs every 10 minutes
    catchup=False,
)

def transform_gcs_files(bucket_name):
   
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # List all files in the bucket
    blobs = list(bucket.list_blobs())
    for blob in blobs:
        # Only process files in the root with content type as 'application/octet-stream' that don't end in '.json'
        if blob.content_type == 'application/octet-stream' and not blob.name.endswith('.json'):
            # Read the content of the file
            file_content = blob.download_as_text()

            try:
                # Load the content as JSON to ensure it's valid
                data = json.loads(file_content)

                # Add default values for missing fields
                data.setdefault('category', 'Unknown')
                data.setdefault('likes', 0)
                data.setdefault('dislikes', 0)
                data.setdefault('comments', 0)
                data.setdefault('publish_time', '1970-01-01T00:00:00Z')

                # Create a new blob in the 'data/' directory with the .json extension
                new_blob_name = f"data/{blob.name}.json"
                new_blob = bucket.blob(new_blob_name)

                # Save the JSON content with correct content type
                new_blob.upload_from_string(json.dumps(data, ensure_ascii=False), content_type='application/json')

                # Optionally, delete the original file to avoid duplicates
                blob.delete()
                print(f"Transformed file {blob.name} to {new_blob_name} and saved in 'data/' directory")

            except json.JSONDecodeError as e:
                print(f"Skipping file {blob.name} as it's not valid JSON: {str(e)}")

# Define the PythonOperator task
transform_task = PythonOperator(
    task_id='transform_gcs_files',
    python_callable=transform_gcs_files,
    op_kwargs={'bucket_name': #bucket name},
    dag=dag,
)

transform_task
