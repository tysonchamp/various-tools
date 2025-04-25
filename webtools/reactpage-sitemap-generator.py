from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET

visited_urls = set()

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    global visited_urls
    urls = set()
    domain_name = urlparse(url).netloc

    options = Options()
    options.headless = True
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        if href.startswith(('tel:', 'mailto:', '#')):
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not href.startswith('http'):
            href = url + href
        if href.endswith("/"):
            href = href[:-1]  # remove trailing slash
        if not is_valid(href):
            continue
        if href in visited_urls:
            continue
        if domain_name not in href:
            continue
        if "/cdn-cgi" in href or "/page/" in href:
            continue
        print(f"Currently scanning: {href}")  # print the URL being scanned
        visited_urls.add(href)
        urls.add(href)
        urls = urls.union(get_all_website_links(href))
    return urls

def generate_sitemap(urls):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url in urls:
        url_element = ET.SubElement(urlset, "url")
        ET.SubElement(url_element, "loc").text = url
    tree = ET.ElementTree(urlset)
    tree.write("sitemap.xml", xml_declaration=True, encoding='utf-8', method="xml")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python reactpage-sitemap-generator.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    urls = get_all_website_links(url)
    generate_sitemap(urls)