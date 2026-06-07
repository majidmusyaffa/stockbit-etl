import time
import json
import random
import pandas as pd
from datetime import date
from extract import get_stock_data
from transform import transform_data
from load import load_to_gcp
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

# List of stocks I want to put in watchlist
list_ticker = ['BRIS', 'ANTM', 'TLKM', 'AMRT']

# Filter the date range
start_date = '2020-01-01'
end_date = str(date.today())

# GCP service account credential path
gcp_cred_path = 'gcp_service_acc_cred.json'
stockbit_cred_path = 'credential.json'

# Create client to GCP
def create_gcp_client(path):
    credentials = service_account.Credentials.from_service_account_file(path)
    project_id = credentials.project_id
    client = bigquery.Client(
        project=project_id,
        credentials=credentials
    )
    dataset_id = f'{project_id}.project_scraping'
    table_id = f'{dataset_id}.daily'

    return client, dataset_id, table_id

client, dataset_id, table_id = create_gcp_client(gcp_cred_path)

job = client.delete_table(table_id)
print(job)