# Airflow ETL Pipeline with Postgres and NASA API Integration

## Project Overview

This project implements an **ETL (Extract, Transform, Load)** pipeline using **Apache Airflow**, which extracts data from NASA's **Astronomy Picture of the Day (APOD) API**, transforms the data, and loads it into a **Postgres** database. The pipeline is orchestrated using **Airflow**, and it utilizes **Docker** to run the services in an isolated and reproducible environment.

### Key Features:
- **Apache Airflow** for orchestrating and scheduling ETL tasks.
- **PostgreSQL** for storing the transformed data.
- **NASA APOD API** to fetch daily astronomy-related data.
- **Docker** for creating an isolated and reproducible environment for both Airflow and Postgres services.

## Objectives

1. **Extract Data**: 
   - Extract astronomy data daily from NASA’s APOD API using the `SimpleHttpOperator`.
   
2. **Transform Data**: 
   - Perform necessary data transformations, such as filtering and processing the JSON response into a usable format.
   
3. **Load Data into Postgres**: 
   - Insert the transformed data into a Postgres database using `PostgresHook` and `PostgresOperator`.

## Architecture and Workflow

The ETL pipeline is orchestrated using an **Airflow DAG**. The process follows three main stages:

### 1. **Extract (E)**:
- **Operator Used**: `SimpleHttpOperator`
- **Task**: Make an HTTP GET request to the NASA APOD API to fetch the astronomy data. The response is in JSON format, containing details like the image title, explanation, and URL.

### 2. **Transform (T)**:
- **Operator Used**: Custom transformation task using Airflow’s **TaskFlow API** (`@task` decorator).
- **Task**: Process the extracted JSON data by:
  - Extracting relevant fields like the title, explanation, image URL, and date.
  - Transforming them into the correct format suitable for insertion into the database.

### 3. **Load (L)**:
- **Operator Used**: `PostgresHook` and `PostgresOperator`
- **Task**: Insert the transformed data into a **Postgres** table. If the table doesn’t exist, it is automatically created as part of the DAG. 


# Deployment Guide

## Prerequisites

- Astro CLI

- VS Code

- Tembo.io account

- AWS account

## Deployment Steps

### 1. Astro UI Deployment

1. Navigate to Astro UI

2. Click Create Deployment

3. Select AWS as target

### 2. VS Code Deployment

```bash

astro  deploy  --dags

```

### 3. PostgreSQL Setup on Tembo

1. Go to Tembo.io

2. Create PostgreSQL instance

3. Save connection details:

- Host

- Login

- Password

- Port

### 4. Airflow Connections

go to airflow ui > admin > connection and set these 2 connections

#### NASA API Connection

```bash

Connection ID: nasa_api

Type: http

Host: https://api.nasa.gov/

Extra: { "api_key": "TLnQfhbikfGL2U1eL6NM6EiAHm1TUT2DfJF2MU1u" }

```

#### PostgreSQL Connection

```bash

Connection ID: postgres_id

Type: Postgres

Host: <Your  Tembo  URL from tembo instance>

Login: <Your  Login from tembo instance>

Password: <Your  Password from tembo instance>

Port: <Your  Port from tembo instance>

Database: postgres

```

### 5. DAG Execution

1. Access Airflow UI

2. Navigate to DAGs

3. Run DAG
