
# **YouTube Data Pipeline with DBT**

## **Overview**
This repository contains a data pipeline project designed to fetch, process, and analyze YouTube data using **Google Cloud**, **DBT**, and **Apache Airflow DAGs** for orchestration. The pipeline automates the ingestion, transformation, and storage of YouTube data, enabling efficient analysis and visualization.

---

## **Project Components**

1. **Data Ingestion**:
   - A custom Python script fetches YouTube data (e.g., video uploads, live streams) using the YouTube Data API.
   - Data is published to Google Cloud Pub/Sub for further processing.

2. **Orchestration**:
   - **Apache Airflow DAGs** manage the pipeline workflow:
     - Fetch data from the YouTube API.
     - Process and store raw data in **Google Cloud Storage (GCS)**.
     - Transform raw data into analytics-ready datasets using **DBT**.

3. **Data Transformation**:
   - **DBT (Data Build Tool)** transforms raw data into clean and structured tables stored in **BigQuery**.

4. **Storage**:
   - **Google Cloud Storage (GCS)**: Stores raw data files in JSON/CSV format.
   - **BigQuery**: Stores processed and transformed datasets.

---

## **Folder Structure**

```
.
├── analyses/         # Custom SQL queries for DBT analyses
├── macros/           # Reusable macros for DBT models
├── models/           # DBT models for data transformation
│   ├── example/      # Example models (replace with project-specific models)
├── seeds/            # Static data loaded into BigQuery
├── snapshots/        # Snapshots for tracking data changes
├── tests/            # Unit tests for DBT models
├── dags/             # Airflow DAGs for pipeline orchestration
│   ├── fetch_data.py # DAG for fetching YouTube data
│   ├── process_data.py # DAG for processing raw data
│   ├── transform_data.py # DAG for running DBT transformations
├── youtube_fetcher/  # Python script for fetching YouTube data via API
├── dbt_project.yml   # Configuration for the DBT project
├── .gitignore        # Git ignore rules
├── README.md         # Project documentation (this file)
```

---

## **How It Works**

### **1. YouTube Data Fetching**
- A Python script (`youtube_fetcher.py`) connects to the YouTube Data API.
- Fetches details like live stream metadata and uploaded videos.
- Publishes raw data to a Google Cloud Pub/Sub topic.

### **2. Pipeline Orchestration**
- Managed by **Apache Airflow** using three DAGs:
  - **`fetch_data.py`**: Fetches YouTube data on a schedule.
  - **`process_data.py`**: Processes raw data and uploads it to GCS.
  - **`transform_data.py`**: Runs DBT models to transform data.

### **3. Data Transformation**
- DBT models in the `models/` directory transform raw data into analysis-ready datasets:
  - **Staging Models**: Cleans and standardizes raw data.
  - **Fact and Dimension Tables**: Aggregates data for reporting and analysis.
- Processed data is stored in **BigQuery**.

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-repo>.git
cd <your-repo>
```

### **2. Install Requirements**
- Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### **3. Set Up Google Cloud**
- Enable the following services:
  - **YouTube Data API**.
  - **Google Cloud Storage**.
  - **BigQuery**.
- Set up authentication:
  - Download the service account key file.
  - Set the environment variable:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="<path_to_service_account_key>"
    ```

### **4. Deploy Airflow DAGs**
- Copy the DAGs to your Airflow DAGs folder:
```bash
cp dags/*.py <AIRFLOW_HOME>/dags/
```
- Start Airflow and trigger the DAGs:
```bash
airflow webserver
airflow scheduler
```

### **5. Execute DBT Models**
- Navigate to the `dbt/` folder.
- Run transformations:
```bash
dbt run
```
- Test the models:
```bash
dbt test
```

---

## **Key Features**
- Automated YouTube data ingestion using the YouTube Data API.
- Pipeline orchestration using Apache Airflow DAGs.
- Scalable transformations and clean datasets using DBT.
- Cloud-native architecture leveraging Google Cloud services.

---

## **Technologies Used**
- **Python**: For scripting and DAGs.
- **Apache Airflow**: For pipeline orchestration.
- **DBT (Data Build Tool)**: For data transformations.
- **Google Cloud**: For storage and data analytics.
  - **BigQuery**: For data warehousing.
  - **Cloud Storage**: For raw data storage.
  - **Pub/Sub**: For message-based data ingestion.
- **YouTube Data API**: For fetching YouTube metadata.

---

## **Future Enhancements**
- Add automated testing for DAGs and DBT models.
- Integrate a dashboard for visualizing YouTube analytics.
- Extend support to other social media APIs.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

