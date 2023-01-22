from pyspark.sql.types import StructType,StructField,StringType,FloatType,IntegerType
import os
import ast

CITIES = ast.literal_eval(os.environ['CITIES'])
S3_ENDPOINT = os.environ['S3_ENDPOINT']
S3_USER = os.environ['S3_USER']
S3_PASSWORD = os.environ['S3_PASSWORD']
SOURCE_BUCKET = os.environ['SOURCE_BUCKET']
SINK_BUCKET = os.environ['SINK_BUCKET']
YEAR = os.environ['YEAR']
MONTH = os.environ['MONTH']
DAY = os.environ['DAY']
JSON_SCHEMA = StructType([StructField('ID' , StringType()),
                          StructField('Type' , StringType()),
                          StructField('Price' , StringType()),
                          StructField('Area' , StringType()),
                          StructField('Purpose' , StringType()),
                          StructField('Beds' , StringType()),
                          StructField('Baths' , StringType()),
                          StructField('Location' , StringType()),
                          StructField('Description' , StringType())])

SINK_SCHEMA = StructType([StructField('ID' , StringType()),
                          StructField('Type' , StringType()),
                          StructField('Price' , FloatType()),
                          StructField('Area' , StringType()),
                          StructField('Purpose' , StringType()),
                          StructField('Beds' , IntegerType()),
                          StructField('Baths' , IntegerType()),
                          StructField('Location' , StringType()),
                          StructField('Description' , StringType())])