from typing import List
import pandas as pd
import requests


class Get:
    """
    The get class will get a single page html data from zameen.com.
    """
    def __init__(self , city , type_property):
        self.city = city
        self.type_property = type_property
        self._BASE_URL_ = 'https://www.zameen.com'
    
    def get_proxies(self) -> List[str]:
        
        """
        This will get random proxies from `https://free-proxy-list.net/` in order to avoid getting banned when scrapping data from zameen.com
        
        Parameters:
        -----------------------
        None

        Returns:
        -----------------------
        proxies(list) --> A list of random proxies


        """
        url = 'https://free-proxy-list.net/'
        html = requests.get(url)
        df_proxies = pd.read_html(html.content)[0]
        df_proxies = df_proxies.loc[(df_proxies['Https'].isin(['yes'])),['IP Address','Port']]
        list_proxies = []
        for _,data in df_proxies.iterrows():
            list_proxies.append(data['IP Address']+':'+str(data['Port']))
        return list_proxies

    def get_index_data(self , index_number:str , proxy:str) -> bytes:
        """
        Method to send request to zamee.com and get the index html page where all their are all of the listings.
        
        Parameters:
        ---------------------------
        index_number(str): The index number which you are requesting for such as 1-1,1-2

        proxy(str): The proxy IP to avoid getting banned

        Returns:
        ---------------------------

        data(bytes): The html data return as bytes for the page

        """

        data = requests.get(f"{self._BASE_URL_}/{self.type_property}/{self.city}-{index_number}.html", proxies = {"http": proxy, "https": proxy})
        if data.status_code != 200:
            print(f'Error: The request returned with status code {str(data.status_code)}')
            return None
        return data.content

    def get_listing(self , url_listing:str , proxy) -> bytes:
        """
        Method to get the data for specific listing for which the url has been provided.

        Parameters:
        ------------------------
        url_listing(str): The url for the listing for which are requesting the data

        proxy(str): The proxy IP to avoid getting banned

        Returns:
        ------------------------
        data(bytes): The html data returned as bytes for the specific listing

        """
        data = requests.get(self._BASE_URL_+'/'+url_listing , proxies = {"http": proxy, "https": proxy})
        if data.status_code != 200:
            print(f'Error: The request returned with status code {str(data.status_code)}')
            return None
        return data.content

