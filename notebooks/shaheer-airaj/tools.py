import os
import logging
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found.")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SearchWeb:
    
    DOMAINS = [
    'https://www.expedia.ae/',
    'https://www.skyscanner.ae/',
    'https://www.etihad.com/en-ae/',
    'https://www.booking.com/'
    ]

    def __init__(self):
        logging.info("\nWeb search tool is being called...\n")
        self.client = TavilyClient(TAVILY_API_KEY)

    def search(self, search_input, include_domains=DOMAINS):
        response = self.client.search(search_input, include_domains=include_domains)
        response_list = [resp["content"] for resp in response["results"]]
        responses = " ".join(response_list)
        return responses