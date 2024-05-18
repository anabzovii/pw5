import argparse
import re
import socket
import requests

from bs4 import BeautifulSoup

def get_webpage(url):
    # Parse the URL to get host and path
    host = url.split('/')[2]
    path = '/' + '/'.join(url.split('/')[3:])

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((host, 80))

    # Send the GET request
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    s.send(request.encode())

    # Receive the response
    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

    # Close the connection
    s.close()

    # Return the response
    return response.decode("utf-8")

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
    print(get_webpage(arguments.call_page_url))
elif arguments.key_word:
    request_viorica(arguments.key_word)