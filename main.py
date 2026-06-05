import time
import json
import random
import pandas as pd
from datetime import date
from extract import get_stock_data
from transform import transform_data
from load import load_to_gcp


# List of stocks I want to put in watchlist
list_ticker = ['BRIS', 'ANTM', 'TLKM', 'AMRT']

# Filter the date range
start_date = '2020-01-01'
end_date = str(date.today())

# GCP service account credential path
gcp_cred_path = 'gcp_service_acc_cred.json'
stockbit_cred_path = 'credential.json'

# Dataframe to collect all of the data
all_df = pd.DataFrame()

for ticker in list_ticker:

    # Extract
    df = get_stock_data(ticker, start_date, end_date, stockbit_cred_path)

    # Transform
    transformed_df = transform_data(df)

    # Combine each dataframe
    all_df = pd.concat([all_df, transformed_df])

    time.sleep(1 + random.gauss(0, 0.1))

# Load
load_to_gcp(all_df, gcp_cred_path)