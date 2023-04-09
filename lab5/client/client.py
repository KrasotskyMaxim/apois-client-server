# python3 client/client.py http://localhost:8080 -m POST -d "data=test"

import argparse
import requests
import logging
import os


logging.basicConfig(filename='./logs/client.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')


def make_request(url, method, headers=None, data=None):
    try:
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err.response.content.decode()}")
        logging.error(f"HTTP Error: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Error Connecting: {err}")
        logging.error(f"Error Connecting: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err}")
        logging.error(f"Timeout Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        logging.error(f"Error: {err}")
    else:
        print(f"Response code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response body: {response.content.decode()}")
        logging.info(f"Response code: {response.status_code}")
        logging.info(f"Response headers: {response.headers}")
        logging.info(f"Response body: {response.content.decode()}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='HTTP client')
    parser.add_argument('url', type=str, help='URL to send request to')
    parser.add_argument('-m', '--method', type=str, default='GET', help='HTTP method')
    parser.add_argument('-d', '--data', type=str, help='Request data')
    parser.add_argument('-f', '--file', type=str, help='File with request data')
    parser.add_argument('-H', '--header', type=str, action='append', help='Request headers')
    args = parser.parse_args()

    url = args.url
    method = args.method.upper()
    headers = {}
    
    if args.file:
        if not os.path.isfile(args.file):
            print('File not found')
            exit(1)
    
        with open(args.file, 'rb') as f:
            data = f.read()
    else:
        data = args.data    
    
    if args.header:
        headers = dict(h.split(':') for h in args.header)

    make_request(url, method, headers=headers, data=data)
