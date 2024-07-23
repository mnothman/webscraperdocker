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

def scrape_website(url):
    if not can_fetch(url):
        print(f"Scraping {url} is not allowed by robots.txt")
        return

# selenium for dynamic js 
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    time.sleep(3)  #delay to allow the page to load

    html_content = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    with open('/app/output/output.csv', 'w', newline='') as csvfile:
        fieldnames = ['link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in links:
            writer.writerow({'link': link.get('href')})

    #delay for server 
    time.sleep(5)

if __name__ == "__main__":
    url = 'https://example.com'
    scrape_website(url)
