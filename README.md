# real_estate_data_platform

## Data Lakehouse Diagram:


## Main Modules (for detailed explanation please open the relevant modules):

### Scrapper ![Click Here](https://github.com/keenborder786/real_estate_data_platform/blob/main/scrapper):

- The scrapper package which we use to scrap data from zameen.com and upload data to minio raw bucket as json files. 


### Spark ![Click Here](https://github.com/keenborder786/real_estate_data_platform/blob/main/spark)

- Spark consist of modules which runs a batch job to process our raw data for a specific city for a given and update the revelant delta table.
- Spark also consist of docker files for master and worker container deployment which will act as spark standalone cluster where our batch job will be running 

### Trinio ![Click Here](https://github.com/keenborder786/real_estate_data_platform/blob/main/trino)

- The main query engine which you can use to query the data from your delta tables.

## How to run the pipeline?

### Build the images:

- Scrapper:

```console
docker build -t scrapper:1.0 -f scrapper/Dockerfile_scrapper .
```
- Spark Base:

```console
docker build -t sparkbase:1.0 -f scrapper/Dockerfile_base .
```
- Spark Client:

```console
docker build -t sparkclient:1.0 -f scrapper/Dockerfile_client .
```
- Spark Master:

```console
docker build -t sparkmaster:1.0 -f scrapper/Dockerfile_master .
```
- Spark Worker:

```console
docker build -t sparkworker:1.0 -f scrapper/Dockerfile_worker .
```

### Starts the s3 bucket,scrapper, spark cluster and trino-coordinator:
    
```console
docker-compose up
```
***Scrapper will start scrapping and uploading the json files to minio bucket on the revelant folder. Therefore please wait before running the spark job as their needs to be some raw data on minio raw bucket for spark to process on otherwise it will just create a empty delta table***

### Start the spark job by launching the spark client(driver):

```console

docker run --net real_estate_data_platform_datapipeline \
--ip 172.18.0.8 --env-file spark/.env.client \
-p 40207:40207 -p 40208:40208 -p 4040:4040 \
-v spark_packages:/root/.ivy2/jars -v spark_cache:/root/.ivy2/cache --name sparkclient sparkclient:1.0

```
***This will intialize our spark job on the containerized spark cluster***
***Once the batch job has been executed, you can query the data from Trino***