# Event Driven Data Platform on Google Cloud

## Overview
This repository implements a cloud native event driven data platform built on Google Cloud. It fetches external API events, ingests them asynchronously, transforms the data into governed analytical tables, and orchestrates continuous processing using Composer.

The system demonstrates:
- decoupled ingestion  
- scalable data processing  
- semantic modeling using DBT  
- automated workflow orchestration  
- secure data warehousing in BigQuery  

---

## Architecture
The platform consists of the following distributed components:

- **API Ingestion Service**
  - Fetches metadata from the YouTube API.
  - Publishes JSON messages to a Google Cloud Pub/Sub topic.

- **Pub/Sub Messaging Backbone**
  - Decouples ingestion from processing.
  - Supports replay, backoff, and scalable parallel consumption.

- **Data Processing & ETL**
  - Raw events are written to Google Cloud Storage.
  - Transformations produce clean structured datasets for analytics.

- **DBT Semantic Modeling**
  - DBT models apply staging, cleaning, and fact dim transformations.
  - Data quality tests validate referential integrity and schema rules.

- **BigQuery Data Warehouse**
  - Stores governed analytics ready tables.
  - Optimized for low cost scans using partitioning and clustering.

- **Cloud Composer (Airflow) Orchestration**
  - Manages scheduling, dependencies, retries, and monitoring signals.

- **Logging and Observability**
  - Pipeline logs captured in GCP logging.
  - DAG execution history enables traceability and incident analysis.

---

## Platform Capabilities
- Asynchronous event ingestion via Pub/Sub  
- Distributed orchestration via Composer  
- Storage layer in GCS and BigQuery  
- Transformations and modeling using DBT  
- Schema validation and testing  
- IAM security with service accounts  
- CI friendly modular structure  

---

## Folder Structure
```text
.
├── analyses/         # DBT analyses and custom queries
├── dags/             # Airflow / Composer DAGs for orchestration
├── macros/           # Reusable DBT macros
├── models/           # DBT models (staging + analytics)
├── seeds/            # Static seed datasets
├── snapshots/        # DBT snapshots for slowly changing data
├── tests/            # DBT tests for data quality
├── fetch.py          # API ingestion script for YouTube data
├── dbt_project.yml   # DBT project configuration
├── .gitignore        # Git ignore rules
└── README.md         # Platform documentation

---

## Workflow
1. Ingestion service publishes events to Pub/Sub.  
2. Raw event payloads are stored in GCS.  
3. Composer coordinates end to end DAG execution.  
4. DBT transforms raw data into clean dimensional tables.  
5. BigQuery enables analytical querying and dashboarding.  

---

## Key Features
- Event driven ingestion (Pub/Sub)  
- Distributed orchestration (Composer)  
- Scalable transformation and modeling (DBT)  
- Analytical storage (BigQuery)  
- Secure access (IAM and service accounts)  
- Robust logging and auditability  

---

## Technologies
- **Python** – ingestion and orchestration logic  
- **Google Cloud Pub/Sub** – event streaming  
- **Cloud Composer (Airflow)** – workflows and orchestration  
- **BigQuery** – governed analytical storage  
- **Google Cloud Storage** – raw data persistence  
- **DBT** – semantic transformations and testing  
- **YouTube Data API** – external data source  

---

## Future Enhancements
- CI workflows for automated DBT testing  
- DAG level metrics emission for monitoring  
- Advanced lineage tracking and metadata cataloging  
- Visualization dashboards  
