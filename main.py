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
from helper import create_dataset, create_table, create_gcp_client, check_bigquery
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

# List of stocks I want to put in watchlist
list_ticker = ['BRIS', 'ANTM', 'TLKM', 'AMRT']

# Filter the date range (start_date is only used for FULL_LOAD)
start_date = '2020-01-01'
end_date = str(date.today())

# GCP service account credential path
gcp_cred_path = 'gcp_service_acc_cred.json'
stockbit_cred_path = 'credential.json'

# Create client to GCP
client, dataset_id, table_id = create_gcp_client(gcp_cred_path)

# Check what load type needed based on history (FULL_LOAD | INCREMENTAL_LOAD | UPDATED)
load_type = check_bigquery(client, dataset_id, table_id)

if load_type['type'] == 'UPDATED':
    print('\nThe latest data has been uploaded')

else:

    # Dataframe to collect all of the data
    all_df = pd.DataFrame()

    for ticker in list_ticker:

        # Extract
        df = get_stock_data(load_type, ticker, stockbit_cred_path, start_date)

        # Transform
        transformed_df = transform_data(df)

        # Combine each dataframe
        all_df = pd.concat([all_df, transformed_df])

        time.sleep(1 + random.gauss(0, 0.1))

    # Load
    load_to_gcp(client, load_type, all_df, table_id)

