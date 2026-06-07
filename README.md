<h1><img src="https://github.com/majidmusyaffa/stockbit-etl/blob/main/assets/saham.webp"></h1>

# Stockbit ETL Pipeline Project

Created an ETL pipeline that takes daily market activity of a stock from Stockbit's internal API. The data collected from Stockbit API is transformed using Pandas and loaded to Google BigQuery.

## Overview

<h1><img src="https://github.com/majidmusyaffa/stockbit-etl/blob/main/assets/etl_diagram.png"></h1>

The ETL Pipeline consist of 3 steps:

- Extract

Data is extracted from Stockbit internal API where the access token needs to be copied manually everyday to the ```credentials.json``` before running the pipeline. The API will return daily market summary of a selected stock where the date range can be changed based on requirement, the result will be transformed into pandas dataframe. There is two types of extraction: full load & incremental load, if the table is empty, full load will be used, if the table is not empty and the latest date in the data is not the latest business date, incremental load will be used.

- Transform

The data transformation consist of fixing data types for certain date column, re-sorting the data based on ascending date, and calculate new columns to see the daily MACD (Moving Average Convergence Divergence) value of the data.

- Load

After Extract & Transform process is done in multiple stocks data, the data will be merged and loaded to Google BigQuery with GCP service account. The dataset and table are already exist, upload data to the table, else define the table schema and create the dataset and table.

## Features

- Extract data saham
- Transform data menggunakan Pandas
- Load data ke BigQuery

## Requirements

- Python 3.10+
- Google Cloud Project
- BigQuery API enabled

## Installation

Clone repository:

```bash
git clone https://github.com/majidmusyaffa/stockbit-etl.git
cd stockbit-etl
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create json file to store your stockbit and GCP service account credentials. I store my stockbit's acces token in ```credential.json``` and my GCP service account credential in ```gcp_service_acc_cred.json```.

My ```credential.json``` file would be like this:
```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIsImtp..."
}
```

And the GCP service account credential in IAM & Admin > Service Accounts > (Choose one of your service account) > Keys > Add keys, it should be like this:

```json
{
  "type": "service_account",
  "project_id": "project-id",
  "private_key_id": "a67ff1f...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nHIIEvgIBAD...-----END PRIVATE KEY-----\n",
  "client_email": "service-acc-name@project-id.iam.gserviceaccount.com",
  "client_id": "12345..",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-acc-name%40project-id.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```


## Run

```bash
python main.py
```

## Result

<h1><img src="https://github.com/majidmusyaffa/stockbit-etl/blob/main/assets/result.png"></h1>

The data is loaded to Google BigQuery.

## Project Structure

```text
stockbit-etl/
├── assets/
├── extract.py
├── transform.py
├── load.py
├── main.py
├── helper.py
├── test.py
├── sample.csv
├── requirements.txt
├── credential.json
├── gcp_service_acc_cred.json
├── .gitignore
└── README.md
```