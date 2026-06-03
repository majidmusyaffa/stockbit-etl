import requests
import json
import pandas as pd
pd.set_option('display.max_columns', None)

def get_stock_data(auth_token, ticker) -> pd.DataFrame:

    url = f'https://exodus.stockbit.com/chartbit/{ticker}/price/daily'

    parameters = {
        'from': '2024-06-22',
        'to': '2023-06-21',
        'limit': 0
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'authorization': 'Bearer ' + auth_token,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'    
    }

    response = requests.get(url, params=parameters, headers=headers)
    data = response.json()['data']['chartbit']
    df = pd.DataFrame(data)
    df['Ticker'] = [ticker for i in range(len(df))]
    
    return df

if __name__ == '__main__':
    with open('credential.json', 'r') as f:
        auth_token = json.load(f)['auth_token']
        print(auth_token)
        df = get_stock_data(auth_token, ticker='BRIS')
        print(df['close'].values)
