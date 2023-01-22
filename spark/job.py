"""

This module is used to connect to our raw bucket and intiate a spark job on given spark cluster
to move all all json files present for a given city for a specific date to the city delta table on
minio delta bucket.

"""

from datetime import datetime
from pyspark.sql import SparkSession,DataFrame
from pyspark.sql.functions import col,udf
from pyspark.sql.types import StructType,FloatType
from delta.tables import DeltaTable

def read_json_data(spark_session:SparkSession , 
                   source_bucket:str ,json_schema:StructType , 
                   city:str , year:str,
                   month:str,day:str) -> DataFrame:
    """
    
    This function is used to read the raw json data for the given city,date and return the json data as 
    spark dataframe.

    Parameters:
    -----------------------------------------------------------

    spark_session(SparkSession): The main spark session to interact with minio

    source_bucket(str): The source bucket where our json data is.

    json_schema(StructType): The schema for our json data

    city(str): The city for which we are getting the data for

    year(str): The year for which we are getting the data for

    month(str): The month for which we are getting the data for

    day(str): The day for which we are getting the data for

    Returns:
    ------------------------------------------------------------
    main_df(DataFrame)

    """
    main_df = spark_session.read.json(f"s3a://{source_bucket}/{city}/{year}/{month}/{day}/*.json" ,
            schema = json_schema)
    return main_df

@udf(returnType = FloatType())
def price_process(x):
    """
    
    A spark user defined function which is used to convert our price string column to integer column
    
    
    """
    if 'Crore' in x:
        return float(x.split('PKR')[-1].split('Crore')[0]) * 1e7
    else:
        return float(x.split('PKR')[-1].split('Lakh')[0]) * 1e5

def process_json_data(df:DataFrame , sink_schema:StructType) -> DataFrame:
    """
    This function is used to process the given dataframe and convert the dataframe columns to the desired schema.

    Parameters:
    -------------------------------

    df(DataFrame): The raw loaded dataframe from json files.

    sink_schema(StructType): The sink schema for dataframe in StructType

    Returns:
    --------------------------------

    df(DataFrame): Final Processed spark dataframe 
    
    
    
    """
    
    schema_json = sink_schema.jsonValue()['fields']
    df = df.withColumn('Price' , price_process(col('Price')))
    for field in schema_json:
        df = df.withColumn(field['name'] , col(field['name']).astype(field['type']))
    return df

def upsert_delta_table(spark_session:SparkSession , df:DataFrame , 
                      sink_bucket:str , table_name:str):
    """
    This is used to upsert the given delta table.

    Parameters:
    -------------------------------------

    spark_session(SparkSession): The main spark session to interact with minio

    df(DataFrame): The processed dataframe to be used to update our delta table.

    sink_bucket(str): The sink bucket name.

    table_name(str): The name of table whose data is being updated.

    Returns:
    --------------------------------------
    None

    
    """

    deltatable_instance = DeltaTable.createIfNotExists(spark_session
             ).location(f"s3a://{sink_bucket}/{table_name}"
             ).tableName(table_name).addColumns(df.schema
             ).execute()
    
    deltatable_instance.alias('main_df').merge(
                        source = df.alias('update_df') ,
                        condition = 'main_df.id = update_df.id'
                        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    






