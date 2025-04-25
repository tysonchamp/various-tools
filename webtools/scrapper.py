import re
import sys
import requests
from bs4 import BeautifulSoup

def scrape_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Regular expressions for phone and email
    phone_re = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    email_re = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    # Find phone numbers and emails
    phones = re.findall(phone_re, soup.text)
    emails = re.findall(email_re, soup.text)

    # Find image URLs
    images = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

    return phones, emails, images

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrapper.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    phones, emails, images = scrape_info(url)
    print('Phones:', phones)
    print('Emails:', emails)
    print('Images:', images)