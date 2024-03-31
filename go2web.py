import argparse
from bs4 import BeautifulSoup
import re
import requests

def create_request(webpage_url):
    return requests.get(webpage_url).text

def request_viorica(key_word):
    search_url = f"https://viorica.md/?s={key_word}"
    viorica_response = requests.get(search_url)
    scrape = BeautifulSoup(viorica_response.text, 'html.parser')

    pattern = r'https://viorica\.md/product/[\w-]+?'
    number_of_item = 1
    for url in scrape.find_all('a'):
        href = url.get('href')
        if href and re.match(pattern, href) and len(url.text.strip()) > 1 and number_of_item < 11:
            print(f"{number_of_item}. {url.text} - {url['href']}")
            number_of_item += 1

argument_reader = argparse.ArgumentParser(description="Help options:")
group = argument_reader.add_mutually_exclusive_group(required=True)
group.add_argument("-u", "--call_page_url", help="Request to a input url")
group.add_argument("-s", "--key_word", help="Find 10 links on the first page from Viorica.md platform")

arguments = argument_reader.parse_args()

if arguments.call_page_url:
    print(create_request(arguments.call_page_url))
elif arguments.key_word:
    request_viorica(arguments.key_word)
