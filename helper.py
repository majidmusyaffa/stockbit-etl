import pandas as pd
from datetime import date, timedelta
from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound



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

def check_bigquery(client, dataset_id, table_id):

    try:
        client.get_dataset(dataset_id)
        print('dataset exist')

        try:
            client.get_table(table_id)
            print('table exist')

            # Search for the latest date
            query = f'''
                    SELECT MAX(date) latest_date
                    FROM {table_id} 
                    '''
            df = client.query(query).to_dataframe()

            latest_date = str(df.values[0][0])
            latest_business_date = get_business_date()

            if (latest_date != latest_business_date):
                return {'type':'INCREMENTAL_LOAD', 'latest_date':latest_date}
            else:
                return {'type':'UPDATED'}

        except NotFound:
            print('table not exist')
            create_table(client, table_id)
            return {'type':'FULL_LOAD'}

    except NotFound:
        print('dataset not exist')
        create_dataset(client, dataset_id)
        create_table(client, table_id)
        return {'type':'FULL_LOAD'}

def create_dataset(client, dataset_id):

    # Create dataset if not exist
    dataset = bigquery.Dataset(dataset_id)
    client.create_dataset(dataset=dataset)

def create_table(client, table_id):

    # Create table if not exist
    schema = [
        bigquery.SchemaField('date', 'DATE'),
        bigquery.SchemaField('unixdate', 'INTEGER'),
        bigquery.SchemaField('open', 'INTEGER'),
        bigquery.SchemaField('high', 'INTEGER'),
        bigquery.SchemaField('low', 'INTEGER'),
        bigquery.SchemaField('close', 'INTEGER'),
        bigquery.SchemaField('volume', 'INTEGER'),
        bigquery.SchemaField('foreignbuy', 'INTEGER'),
        bigquery.SchemaField('foreignsell', 'INTEGER'),
        bigquery.SchemaField('soxclose', 'INTEGER'),
        bigquery.SchemaField('dividend', 'FLOAT64'),
        bigquery.SchemaField('value', 'INTEGER'),
        bigquery.SchemaField('shareoutstanding', 'INTEGER'),
        bigquery.SchemaField('freq_analyzer', 'FLOAT64')
    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)


def get_business_date():
    today = date.today()

    if today.weekday() > 4:
        today -= timedelta(days=today.weekday() - 4)

    return today.strftime("%Y-%m-%d")