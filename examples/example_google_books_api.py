"""
Purpose : simple example showing how to retrieve a title from using the Google Books API
Date : 11/7/2020

Notes :
- maxResults set to 20 (pagination not implemented)
- Saved API key from https://console.developers.google.com/apis/credentials?project=tech-book-collection&supportedpurview=project
in local machine under ~/.api_keys
- API search Keys:
    publisher
    description
    language
    publishedDate
    readingModes
    previewLink
    title
    printType
    infoLink
    pageCount
    maturityRating
    contentVersion
    industryIdentifiers
    imageLinks
    authors
    canonicalVolumeLink
    ratingsCount
    allowAnonLogging
    panelizationSummary
    categories
    averageRating

References:
    Books API: https://developers.google.com/books/docs/v1/using

TODO:
- [BUG] Categories search returns for a single author

"""
# imports
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from urllib import urlencode
import logging

# globals
API_KEY_PATH = sys.argv[1]
# 'intitle': 'flowers'} "TITLE" # title/isbn/author/category
GOOG_BOOKS_HOST = "https://www.googleapis.com/books/v1/volumes"

# helper functions
def setup_logger(log_file_name):
	logger = logging.basicConfig(filename=log_file_name,
                        		 level=logging.DEBUG,
                        		 format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ]: %(message)s',
                        		 datefmt='%m/%d/%Y %I:%M:%S %p')
	return logger



def parse_api_key_file(file):
    with open(file) as api_file:
        api_key = json.load(api_file).get('api_key').encode('utf-8')
	return api_key

def validate_search_field(_field, _value):
	is_valid = False
	if _field.upper() in ['TITLE', 'AUTHOR', 'ISBN', 'CATEGORY'] and _value is not None:
		is_valid = True
	return is_valid

def make_http_request(url, key, query):
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth('apikey', key)
    resp = requests.get(url,
                        headers=headers,
                        auth=auth,
                        params={'q': query,
                                'maxResults': 20}).json()
    return resp

def show_data(data):
    title_list=[]
    if data.get('items'):
        for item in data['items']:
            title = item.get('volumeInfo').get('title')
            if title in title_list:
                continue
            else:
                title_list.append(title)
            author=",".join(data['items'][0].get('volumeInfo').get('authors'))

            print("{},{}".format(title.encode('utf-8'), author.encode('utf-8')))
    else:
        raise RequestException('Search did not return anything! .. ')

    return

# main
if __name__ == '__main__':
    # setup logging
    setup_logger(log_file_name='sample_books_api.log')

    # Get API key to use
    api_key = parse_api_key_file(file=API_KEY_PATH)

    # Make an HTTP request and retrieve data
    key = input('Enter search key:([TITLE, AUTHOR, ISBN, CATEGORY])')
    value = input("Enter value: ")
    SEARCH_QUERY_DICT = {str(key): str(value)}
    data = make_http_request(url=GOOG_BOOKS_HOST, key=api_key, query=urlencode(SEARCH_QUERY_DICT).replace("=", ":"))

    # Show data
    show_data(data)
