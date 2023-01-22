import os

NUMBER_OF_REQUESTS = int(os.environ['NUMBER_OF_REQUESTS'])
SCRAPE_PAGES = int(os.environ['SCRAPE_PAGES'])
CITY = os.environ['CITY']
TYPE = os.environ['TYPE']
SLEEP_INTERVAL =  int(os.environ['SLEEP_INTERVAL'])
S3_ENDPOINT = os.environ['S3_ENDPOINT']
S3_USER = os.environ['S3_USER']
S3_PASSWORD = os.environ['S3_PASSWORD']
STARTING_PAGE = int(os.environ['STARTING_PAGE'])