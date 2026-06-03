import pandas as pd

#a = [-1, 2, 3, 4, 5, 2, 1, -3, -5, -10]
#price = [1000, 2000, 3000, 2500, 2000, 1000, 900, 800,900,1000]


def generate_EMA_sequence(price_data, period: int) -> list:
    list_EMA = [price_data[0]]
    alpha = 2/(period+1)

    latest_EMA = price_data[0]
    for i in range(1, len(price_data)):
        current_EMA = alpha * price_data[i] + (1 - alpha) * latest_EMA
        list_EMA.append(current_EMA)
        latest_EMA = current_EMA

    return list_EMA

def transform_data(df:pd.DataFrame) -> pd.DataFrame:

    # Change data type of date from string to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].dt.date

    # Sort date to ascending because the original data from the API source are descending
    df.sort_values('date', ascending=True, inplace=True)

    # Reset index after sorted
    df.reset_index(drop=True, inplace=True)

    # Generate MACD data
    list_EMA_12 = generate_EMA_sequence(df['close'].values, 12)
    list_EMA_26 = generate_EMA_sequence(df['close'].values, 26)
    list_MACD = [list_EMA_12[i] - list_EMA_26[i] for i in range(len(list_EMA_12))]
    list_signal_MACD = generate_EMA_sequence(list_MACD, 9)
    list_MACD_difference = [list_MACD[i] - list_signal_MACD[i] for i in range(len(list_MACD))]

    df['MACD'] = list_MACD
    df['Signal_MACD'] = list_signal_MACD
    df['MACD_difference'] = list_MACD_difference

    return df

if __name__ == '__main__':
    from extract import get_stock_data
    import json
    with open('credential.json', 'r') as f:
        auth_token = json.load(f)['auth_token']
        df = get_stock_data(ticker='BRIS', start='2025-01-01',end='2025-02-01',cred_path='credential.json')
        transformed_df = transform_data(df)
        transformed_df.head(10).to_csv('test.csv')
