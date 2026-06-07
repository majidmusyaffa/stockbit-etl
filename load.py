import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


def load_to_gcp(client, load_type:dict, df:pd.DataFrame, table_id:str) -> None:

    table = client.get_table(table_id)

    # Create job to batch load data
    if (load_type['type'] == 'FULL_LOAD'):
        write_disp = 'WRITE_TRUNCATE'
    elif load_type['type'] == 'INCREMENTAL_LOAD':
        write_disp = 'WRITE_APPEND'
    job_config = bigquery.LoadJobConfig(
        schema = table.schema,
        write_disposition=write_disp 
    )

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Wait until done
    job.result()

    print(f"Loaded {job.output_rows} rows")