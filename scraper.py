import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re
import logging
from database import create_database, save_to_database

#logging
logging.basicConfig(filename='/app/output/scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


#respect robots.txt
def can_fetch(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"
    
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            user_agent = '*'
            is_allowed = True
            
            for line in lines:
                if line.startswith('User-agent:'):
                    user_agent = line.split(':')[1].strip()
                if user_agent == '*' and line.startswith('Disallow:'):
                    disallowed_path = line.split(':')[1].strip()
                    disallowed_pattern = re.compile(disallowed_path.replace('*', '.*'))
                    if disallowed_pattern.match(parsed_url.path):
                        is_allowed = False
                        break
            return is_allowed
        else:
            return True
    except requests.RequestException:
        return True


def scrape_page(url, page):
    try:
        if not can_fetch(url):
            logging.warning(f"Scraping {url} is not allowed by robots.txt")
            return []

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        time.sleep(3)  #page loading

        html_content = driver.page_source
        driver.quit()

        soup = BeautifulSoup(html_content, 'html.parser')
        items = soup.find_all('div', class_='item')

        data = []
        for item in items:
            title = item.find('h2').text
            description = item.find('p').text
            data.append((title, description, page))

        logging.info(f"Successfully scraped {url}")

        time.sleep(5) #server delay
        return data
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
        return []

def scrape_website(base_url, pages=5):
    db_path = '/app/output/data.db'
    create_database(db_path)
    
    with open('/app/output/output.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'description', 'page']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(1, pages + 1):
            paginated_url = f"{base_url}?page={page}"
            data = scrape_page(paginated_url, page)
            if data:
                writer.writerows(data)
                save_to_database(db_path, data)

if __name__ == "__main__":
    url = 'https://example.com'
    scrape_website(url, pages = 5)
