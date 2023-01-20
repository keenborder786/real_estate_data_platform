from scrapper_package.get_data import Get
from scrapper_package.parse_data import Parse
from scrapper_package.util import bucket_creation
from itertools import cycle
from datetime import datetime
from scrapper_package.config import (
        NUMBER_OF_REQUESTS,
        SCRAPE_PAGES,
        CITY,
        TYPE,
        SLEEP_INTERVAL,
        S3_ENDPOINT,
        S3_USER,
        S3_PASSWORD
        )
from minio import Minio
import requests
import json
import time
import io

print(f""" 
    Scrapper is being started with the following config:
    NUMBER_OF_REQUESTS --- {NUMBER_OF_REQUESTS}
    SCRAPE_PAGES --- {SCRAPE_PAGES}
    CITY --- {CITY}
    TYPE --- {TYPE}
    SLEEP_INTERVAL --- {SLEEP_INTERVAL}
    """)

get_instance = Get(CITY , TYPE)
parse_instance = Parse()
list_proxy = get_instance.get_proxies()
proxy_pool = cycle(list_proxy)
client = Minio(
    S3_ENDPOINT,
    access_key=S3_USER,
    secret_key=S3_PASSWORD,
    secure=False
) 
bucket_creation('raw' , client) ## Create the desired bucket
dateTimeObj = datetime.now()
all_links_ids = []
connection_error = False
last_page = 1

### First get all the links for all of the listings in all of the pages.
for _ in range(NUMBER_OF_REQUESTS):
    random_proxy = next(proxy_pool)## Take a random proxy
    try:### Making sure that the given proxy works
        response = requests.get('https://www.zameen.com' , proxies = {"http": random_proxy, "https": random_proxy})
    except:
        print("Skipping. Connnection error")
        continue
    print(f'Connection established with the following proxy {random_proxy}')
    for page in range(last_page, SCRAPE_PAGES+1):### Start from the given page till the number of pages you would like to scrape for
        print('*** Getting Links for Page {} ***'.format(page))
        try:
            index_data = get_instance.get_index_data('1-{}'.format(str(page)) , random_proxy) ## Get the index page data
        except requests.exceptions.ProxyError: ## If their is proxy error then flag the connection error
            print("Exception Proxy Error")
            connection_error = True
            break
        if index_data == None:## If index_data none then we have experienced a error and would like to break out of the loop
            connection_error = True
            break
        url_indexes_current_page = parse_instance.parse_main_index(index_data)## Take the urls and ids for the listing on the given page
        all_links_ids.extend(url_indexes_current_page)## Inserting urls and ids
        time.sleep(SLEEP_INTERVAL)## Interval to avoid getting soft ban
    
    if connection_error:
        last_page = page
        connection_error = False ## Reverting back to False for the connection Error
    else:## If no error was experienced then this mean you don't need to try another proxy
        break
print('*** Pages URL(s) were succesfully feteched ***')
list_proxy = get_instance.get_proxies() ## Refreshing the proxies to avoid getting banned.
last_listing_index = 0 ## Starting from the first listing

## Now at this point in time we have all of the links and ids. We would like to know get the revelant for each of the id and link.
for _ in range(NUMBER_OF_REQUESTS):
    random_proxy = next(proxy_pool)## Take a random proxy
    try:### Making sure that the given proxy works
        response = requests.get('https://www.zameen.com' , proxies = {"http": random_proxy, "https": random_proxy})
    except:
        print("Skipping. Connnection error")
        continue
    print(f'Connection established with the following proxy {random_proxy}')
    for current_listing_index in range(last_listing_index , len(all_links_ids)):
        url , id = all_links_ids[current_listing_index]
        try:
            listing_data = get_instance.get_listing(url , random_proxy)
        except requests.exceptions.ProxyError: ## If their is proxy error then flag the connection error
            print("Exception Proxy Error")
            connection_error = True
            break
        if listing_data == None:
            connection_error = True
            break
        json_data = parse_instance.parse_main_listing(listing_data ,id, ['Type' ,'Price', 'Area','Purpose','Beds','Baths','Location']) ## Parse the listing data
        json_data_bytes  = json.dumps(json_data).encode('utf-8')
        if json_data == None: continue  ## json_data is None then this mean this is a type of listing we don't need. 
        print(f'*** Data was fetched for the ID {id} and now uploading to minio ***')
        client.put_object(bucket_name = 'raw' , 
        object_name = f"{CITY}/{dateTimeObj.year}/{dateTimeObj.month}/{dateTimeObj.day}/{id}.json", 
        data = io.BytesIO(json_data_bytes)  , 
        length = len(json_data_bytes)) ## Upload the data to minio
        
        print(f'*** Data was fetched for the ID {id} has been uploaded to minio ***')
        time.sleep(SLEEP_INTERVAL) ## To avoid getting banned
    
    if connection_error:
        last_listing_index = current_listing_index
        connection_error = False ## Reverting back to False for the connection Error
    else:## If no error was experienced then this mean you don't need to try another proxy  
        break
    
