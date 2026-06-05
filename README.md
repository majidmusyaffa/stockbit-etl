<h1><img src="https://github.com/majidmusyaffa/stockbit-etl/blob/main/assets/saham.webp"></h1>

# Stockbit ETL Pipeline Project

Created an ETL pipeline that takes daily market activity of a stock from Stockbit's internal API. The data collected from Stockbit API is transformed using Pandas and loaded to Google BigQuery.

## Overview

<h1><img src="https://github.com/majidmusyaffa/stockbit-etl/blob/main/assets/etl_diagram.png"></h1>

The ETL Pipeline consist of 3 steps:

- Extract

Data is extracted from Stockbit internal API where the access token needs to be copied manually everyday to the ```credentials.json``` before running the pipeline. The API will return daily market summary of a selected stock where the date range can be changed based on requirement, the result will be transformed into pandas dataframe.

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
git clone https://github.com/username/stockbit-etl.git
cd stockbit-etl
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Buat file credential Google Cloud dan simpan di lokasi yang aman.

Contoh:

```text
credentials/service-account.json
```

File tersebut tidak disertakan dalam repository.

## Run

```bash
python main.py
```

## Project Structure

```text
stockbit-etl/
├── data/
├── src/
├── requirements.txt
├── .gitignore
└── README.md
```