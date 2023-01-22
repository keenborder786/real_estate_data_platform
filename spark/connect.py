"""

This module is used to make a connection to s3 bucket called raw

"""

from pyspark.sql import SparkSession
import pyspark

def make_connection(endpoint:str, user:str , password:str) -> SparkSession:
    """
    Parameters:
    -------------------------------------------------
    endpoint(str): The endpoint to access minio.

    user(str): The user with access to minio.

    password(str): The password for the user with access to minio

    Returns:
    --------------------------------------------------
    SparkSession: SparkSession with connection to minio

    """
    
    spark = SparkSession.builder.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    ).appName("Spark-Real-Estate"
    ).getOrCreate()
    
    spark.sparkContext.setSystemProperty(
        "com.amazonaws.services.s3.enableV4", "true")
    spark.sparkContext.setLogLevel("Error")
    hadoop_config = {
        "fs.s3a.endpoint": endpoint,
        "fs.s3a.access.key": user,
        "fs.s3a.secret.key": password,
        "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        "spark.hadoop.fs.s3a.path.style.access": "true",
        "com.amazonaws.services.s3.enableV4": "true",
        "fs.s3a.connection.ssl.enabled": "false",
        "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
    }
    for k, v in hadoop_config.items():
        spark.sparkContext._jsc.hadoopConfiguration().set(k, v)
    return spark