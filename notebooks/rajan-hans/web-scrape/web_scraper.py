import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import streamlit as st

class WebScraper:
    def __init__(self, driver_path=None):
        """
        Initialize the scraper.
        :param driver_path: Optional path to the ChromeDriver executable.
        """
        self.driver_path = driver_path

    def get_url_text(self):
        """
        Uses Selenium to fetch raw text from the travel destination URL.
        """
        urls = {
            'tandl': 'https://www.travelandleisure.com/wba-2024-cities-world-8660857'
        }
        driver = webdriver.Chrome(self.driver_path) if self.driver_path else webdriver.Chrome()
        driver.get(urls['tandl'])
        time.sleep(5)  # Allow time for the page to load
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        driver.quit()
        return body_text

    def extract_ranked_cities(self):
        """
        Scrapes the page and extracts ranked city and country data using regex.
        Returns:
            List of strings in the format "rank - city, country"
        """
        pattern = r"(?m)^(\d+)\.\s+(.*?),\s+(.*)$"
        body_text = self.get_url_text()
        matches = re.findall(pattern, body_text)
        results = [f"{rank} - {city}, {country}" for (rank, city, country) in matches]
        return results

# Cache the scraped results. This function will run only once per cache cycle.
@st.cache_data(show_spinner=False)
def get_cached_ranked_cities(driver_path=None):
    scraper = WebScraper(driver_path)
    return scraper.extract_ranked_cities()
