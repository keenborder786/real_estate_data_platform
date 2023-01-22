from connect import make_connection
from datetime import datetime
from job import read_json_data , process_json_data , upsert_delta_table
from util import bucket_creation
from minio import Minio
from config import (
                CITIES,
                S3_ENDPOINT,
                S3_USER,
                S3_PASSWORD,
                SOURCE_BUCKET,
                SINK_BUCKET,
                YEAR,
                MONTH,
                DAY,
                JSON_SCHEMA,
                SINK_SCHEMA)

client = Minio(
    S3_ENDPOINT,
    access_key=S3_USER,
    secret_key=S3_PASSWORD,
    secure=False
) 
spark_session = make_connection(S3_ENDPOINT , S3_USER , S3_PASSWORD) ## You create the spark session
for city in CITIES: ## You iterate over which city for which you want to update date for
    print("*** Updating Data for the following city {} *** ".format(city))
    df_raw = read_json_data(spark_session , SOURCE_BUCKET ,JSON_SCHEMA , city , YEAR, MONTH, DAY) ### Read the Raw JSON Data
    bucket_creation(SINK_BUCKET , client) ## Create the Processed Bucket
    df_processed = process_json_data(df_raw , SINK_SCHEMA) ## Processed the Raw Data
    upsert_delta_table(spark_session , df_processed , SINK_BUCKET , f'Fact_{city}_Data') ## Upsert the table

