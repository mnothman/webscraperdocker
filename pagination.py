import requests
from urllib.parse import urljoin
import xml.etree.ElementTree as ET
import logging

#default to w.e pages if no sitemap found
DEFAULT_PAGES = 5

#get xml to see how many pages
def get_sitemap_urls(base_url):
    sitemap_urls = []
    possible_sitemaps = [urljoin(base_url, 'sitemap.xml'), urljoin(base_url, 'sitemap_index.xml')]
    
    for sitemap_url in possible_sitemaps:
        try:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                sitemap_urls.append(sitemap_url)
                break
        except requests.RequestException:
            continue
    return sitemap_urls

def parse_sitemap(sitemap_url):
    urls = []
    try:
        response = requests.get(sitemap_url)
        tree = ET.ElementTree(ET.fromstring(response.content))
        root = tree.getroot()
        for elem in root:
            for subelem in elem:
                if 'loc' in subelem.tag:
                    urls.append(subelem.text)
    except Exception as e:
        logging.error(f"Error parsing sitemap: {e}")
    return urls

def get_total_pages(base_url):
    sitemap_urls = get_sitemap_urls(base_url)
    if not sitemap_urls:
        logging.error("No sitemap found.")
        return DEFAULT_PAGES #if no xml page found with number of pages inside of it, then default to however many pages
    all_urls = []
    for sitemap_url in sitemap_urls:
        all_urls.extend(parse_sitemap(sitemap_url))
    return len(all_urls) if all_urls else DEFAULT_PAGES #deal with default pages 
