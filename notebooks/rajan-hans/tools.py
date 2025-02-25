
import logging
import wikipedia
from tavily import TavilyClient




logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SearchWeb():
    
    DOMAINS = [
    'https://www.expedia.ae/',
    'https://www.skyscanner.ae/',
    'https://www.booking.com/',
    'https://www.tripadvisor.com/',
    'https://www.hotels.com/',
    'https://www.airbnb.com/',
    'https://www.kayak.com/',
    'https://wikitravel.org/',
    'https://wikipedia.com'
    ]

    def __init__(self, tavily_api_key):
        logging.info("Web search tool is being called...")
        self.tavily_api_key = tavily_api_key
        self.client = TavilyClient(self.tavily_api_key)

    def search(self, search_input, include_domains=DOMAINS):
        response = self.client.search(search_input, include_domains=include_domains, lang="en",search_depth="advanced")
        response_list = [resp["content"] for resp in response["results"]]
        responses = " ".join(response_list)
        return responses

#below tools are defined but not used in the code    
class SearchWiki:
    
    DOMAINS = [
    'https://wikitravel.org/',
    'https://wikipedia.com'
    ]

    def __init__(self):
        logging.info("Wiki search tool is being called...")
        
    def searchwiki(self, search_input, include_domains=DOMAINS):
        response = self.client.search(search_input, include_domains=include_domains)
        response_list = [resp["content"] for resp in response["results"]]
        responses = " ".join(response_list)
        return responses    
    
class SearchWeather:
    
    DOMAINS = [
    'https://weather.com/',
    'https://www.accuweather.com/'
    ]

    def __init__(self):
        logging.info("Weather search tool is being called...")
        
    def searchweather(self, search_input, include_domains=DOMAINS):
        response = wikipedia.summary(search_input, sentences=5)
        #response = self.client.search(search_input, include_domains=include_domains)
        response_list = [resp["content"] for resp in response["results"]]
        responses = " ".join(response_list)
        return responses    