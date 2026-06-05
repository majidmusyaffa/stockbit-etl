import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

def load_to_gcp(df:pd.DataFrame, service_account_path:str) -> None:

    credentials = service_account.Credentials.from_service_account_file(service_account_path)
    project_id = credentials.project_id
    client = bigquery.Client(
        project=project_id,
        credentials=credentials
    )
    dataset_id = f'{project_id}.project_scraping'
    table_id = f'{dataset_id}.daily'

    # Create dataset if not exist
    dataset = bigquery.Dataset(dataset_id)
    client.create_dataset(dataset=dataset, exists_ok=True)

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
    table = client.create_table(table, exists_ok=True)
    

    # Create job to batch load data
    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition='WRITE_TRUNCATE'
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Wait until done
    job.result()

    print(f"Loaded {job.output_rows} rows")