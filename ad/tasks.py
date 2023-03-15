from google.cloud import bigquery
import google.auth
from google.ads.googleads.client import GoogleAdsClient

from random import randint, uniform
import pandas as pd
from invoke import task
import django

import os 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adtask.settings")
django.setup()

def insert_ads_data():
    """
    Inserts ads data into BigQuery
    """
    # Create a list of rows to insert
    rows = []
    for i in range(10):

        name = 'Ad ' + str(i)
        impressions = randint(10, 1000)
        clicks = randint(1, impressions)
        cost = round(uniform(1.0, 10.0), 2)
        conversions = int(round(clicks * uniform(0.01, 0.1), 0))
        revenue = round(cost * uniform(0.1, 0.5), 2)
        rows.append({
            'name': name, 
            'impressions': impressions, 
            'clicks': clicks, 
            'cost': cost, 
            'conversions': conversions, 
            'revenue': revenue
        })

    # Write data to a local file (Using file to load data into BigQuery to avoid 403 error for free tier)
    file_name = 'ads_data.csv'
    with open(file_name, 'w') as f:
        header = ['name', 'impressions', 'clicks', 'cost', 'conversions', 'revenue']
        f.write(','.join(header) + '\n')
        for row in rows:
            f.write(','.join([str(value) for value in row.values()]) + '\n')

    # Load the data from the file into BigQuery
    project_id = 'wildnet-379515'
    dataset_name = 'test_dataset'
    table_name = 'GoogleAds'
    client = bigquery.Client(project=project_id)
    dataset_ref = client.dataset(dataset_name)
    table_ref = dataset_ref.table(table_name)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    with open(file_name, 'rb') as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    job.result()

    print('Data loaded successfully')


"""
Mehod to update the BigQuery table with the metrics CPA, CPC, and ROAS
"""
def update_ad_metrics():
    # Connect to the BigQuery client and retrieve the table "GoogleAds"
    client = bigquery.Client()

    # Add new columns for the metrics CPA, CPC, and ROAS in the table schema
    table_ref = client.dataset('test_dataset').table('GoogleAds')
    table = client.get_table(table_ref)
    schema_updates = []
    for field in ['cpa', 'cpc', 'roas']:
        if field not in [f.name for f in table.schema]:
            schema_updates.append(bigquery.SchemaField(field, 'FLOAT', mode='NULLABLE'))
    if schema_updates:
        table.schema += schema_updates
        table = client.update_table(table, ['schema'])

    # Create a new table to store the calculated metrics
    new_table_ref = client.dataset('test_dataset').table('GoogleAdsMetrics')
    new_table = bigquery.Table(new_table_ref, schema=[
        bigquery.SchemaField('name', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('cpa', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('cpc', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('roas', 'FLOAT', mode='NULLABLE')
    ])
    client.create_table(new_table)

    # Query the original table to retrieve the necessary data for the metrics calculation
    query_job = client.query("""
        SELECT name, clicks, cost, conversions, revenue
        FROM test_dataset.GoogleAds
    """)
    results = query_job.result()

    # Calculate the metrics for each row of data and insert the calculated metrics into the new table
    insert_rows = []
    for row in results:
        cpa = row.cost / row.conversions if row.conversions else 0
        cpc = row.cost / row.clicks if row.clicks else 0
        roas = row.revenue / row.cost if row.cost else 0
        insert_rows.append((row.name, cpa, cpc, roas))

    if insert_rows:
        # Insert the calculated metrics into the new table using batch insert
        df = pd.DataFrame(insert_rows, columns=['name', 'cpa', 'cpc', 'roas'])
        job_config = bigquery.LoadJobConfig()
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        job = client.load_table_from_dataframe(df, new_table, job_config=job_config)
        job.result()

    # Join the new table with the original table and update the metrics
    join_query = f"""
        UPDATE test_dataset.GoogleAds
        SET cpa = metrics.cpa, cpc = metrics.cpc, roas = metrics.roas
        FROM test_dataset.GoogleAdsMetrics metrics
        WHERE test_dataset.GoogleAds.name = metrics.name AND test_dataset.GoogleAds.date = metrics.date
    """
    join_job_config = bigquery.QueryJobConfig()
    join_job_config.dry_run = True  # Set to True to check if the query is valid
    join_query_job = client.query(join_query, job_config=join_job_config)
    if join_query_job.errors:
        raise Exception(f"Join query error: {join_query_job.errors}")
    else:
        join_query_job_config = bigquery.QueryJobConfig()
        join_query_job_config.dry_run = False  # Set to False to actually execute the query
        join_query_job = client.query(join_query, job_config=join_query_job_config)
        join_query_job.result()

    print('Metrics updated successfully')

"""
Method to pause ad 
"""
def pause_ad(client, ad_id):
    ad_service = client.service("AdService")
    ad_operation = client.get_type("AdOperation")
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(client.customer_id, ad_id)
    ad.status = client.get_type("AdStatusEnum").PAUSED
    ad_response = ad_service.mutate_ads(
        customer_id=client.customer_id, operations=[ad_operation]
    )
    print(f"Paused ad with ID {ad_response.results[0].resource_name}")

"""
Method to unpause ad 
"""
def unpause_ad(client, ad_id):
    ad_service = client.service("AdService")
    ad_operation = client.get_type("AdOperation")
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(client.customer_id, ad_id)
    ad.status = client.get_type("AdStatusEnum").ENABLED
    ad_response = ad_service.mutate_ads(
        customer_id=client.customer_id, operations=[ad_operation]
    )
    print(f"Unpaused ad with ID {ad_response.results[0].resource_name}")

"""
Method to update ad
"""
def update_ad(client, ad_id, attribute1, attribute2):
    ad_service = client.service("AdService")
    ad_operation = client.get_type("AdOperation")
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(client.customer_id, ad_id)
    ad.headline = attribute1
    ad.description = attribute2
    ad_response = ad_service.mutate_ads(
        customer_id=client.customer_id, operations=[ad_operation]
    )
    print(f"Updated ad with ID {ad_response.results[0].resource_name}")

"""
Method to fetch ads data from BigQuery table `GoogleAds`
"""
def fetch_ads():
    client = bigquery.Client()
    
    # Fetch ads data from BigQuery table `GoogleAds`
    ads = client.query("""
        SELECT id, name, status, headline, description  
        FROM test_dataset.GoogleAds
    """).result()

    return ads

"""
Invoke task to insert ads data into BigQuery
"""
@task
def insert_data(ctx):
    insert_ads_data()

"""
Invoke task to calculate metrics for ads and update the BigQuery table `GoogleAds`
"""
@task
def calculate_matrix(ctx):
    update_ad_metrics()

"""
Invoke task to pause ads
"""
@task
def pause_ad_task(ctx):
    """
    Steps:
    1. Fetch ads data from BigQuery table `GoogleAds`
    2. Pause ads
    """

    credentials, _ = google.auth.default()
    client = GoogleAdsClient(credentials=credentials)

    # Fetch ads data from BigQuery table `GoogleAds`
    ads = fetch_ads()

    # Pause ads
    for ad in ads:
        pause_ad(client, ad.id)
   

"""
Invoke task to unpause ads
"""
@task
def unpause_ad_task(ctx):
    """
    1. Fetch ads data from BigQuery table `GoogleAds`
    2. Unpause ads
    """

    credentials, _ = google.auth.default()
    client = GoogleAdsClient(credentials=credentials)

    # Fetch ads data from BigQuery table `GoogleAds`
    ads = fetch_ads()

    # Unpause ads
    for ad in ads:
        unpause_ad(client, ad.id)
    

"""
Invoke task to update ads
"""
@task
def update_ad_task(ctx):
    """
    1. Fetch ads data from BigQuery table `GoogleAds`
    2. Update ads
    """

    credentials, _ = google.auth.default()
    client = GoogleAdsClient(credentials=credentials)

    # Fetch ads data from BigQuery table `GoogleAds`
    ads = fetch_ads()

    # Update ads
    for ad in ads:
        update_ad(client, ad.id, "New Headline", "New Description")





