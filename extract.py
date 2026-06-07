import requests
import json
import pandas as pd
from datetime import date

def get_stock_data(load_type:dict, ticker:str, cred_path:str, 
                   full_load_start_date:str) -> pd.DataFrame:

    with open(cred_path, 'r') as f:
        auth_token = json.load(f)['auth_token']

    url = f'https://exodus.stockbit.com/chartbit/{ticker}/price/daily'

    if load_type['type'] == 'FULL_LOAD':
        start_date = full_load_start_date
    elif load_type['type'] == 'INCREMENTAL_LOAD':
        start_date = load_type['latest_date']

    today = date.today()
    parameters = {
        'from': today,
        'to': start_date,
        'limit': 0
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer ' + auth_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'    
    }

    print(f'Extracting {ticker}...')

    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()['data']['chartbit']
    df = pd.DataFrame(data)
    df['Ticker'] = [ticker for i in range(len(df))]

    print(f'Collected {len(df)} records.')

    return df

