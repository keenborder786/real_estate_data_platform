
import requests
from bs4 import BeautifulSoup as bs
from typing import List,Dict,Tuple

class Parse:
    """
    The parse class will parase the html data through beautiful soup lib. 
    """
   
    def parse_main_index(self , data:bytes) -> List[Tuple[str , str]]:
        """
        This method will parse the data on main index and will return all of the link of listing mentioned on the given page.

        Parameters:
        ------------------------

        data(byte): Html byte content for the main index page

        Returns:
        ------------------------

        all_urls(list): The list of urls on the index page of zameen and respective ids for each of the listing.

        
        
        """
        b4_instance = bs(data , 'html.parser')
        listing_link_data = b4_instance.find_all('a' , attrs={"aria-label":"Listing link"})
        all_urls_ids = [(x['href'],x['href'].split('-')[1]) for x in listing_link_data]
        return all_urls_ids
    

    def parse_main_listing(self , data:bytes , id:str , attributes:List[str]) -> Dict:
        """
        
        
        
        """
        b4_instance = bs(data , 'html.parser')
        
        property_details = b4_instance.find(attrs={"aria-label":"Property details"})
        property_description = b4_instance.find(attrs={"aria-label":"Property description"})
        if property_details == None: 
            print(f"No Relevant data was found for ID {id}")
            return None
        final_json = {'ID':id}
        for attribute in attributes:
            final_json[attribute] = property_details.find(attrs={"aria-label":attribute}).text
        if property_description != None:
            final_json['Description'] = property_description.text
        else:
            final_json['Description'] = ''
        return final_json
        



        


        



