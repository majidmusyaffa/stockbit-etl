# Stockbit ETL

ETL pipeline untuk mengambil data saham dan menyimpannya ke Google BigQuery.

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