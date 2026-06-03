import pandas as pd
from extract import get_stock_data

df = pd.DataFrame()


print(df.head(5))
print(df.info())

df['date'] = pd.to_datetime(df['date'])

print(df.info())