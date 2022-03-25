import requests
import re
import logging

def fetch_hotsearch():
    url = "https://i.snssdk.com/hot-event/hot-board/?origin=hot_board"
    headers = {}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    hot_searches = []

    for band in data:
        try:
            item = {
                'content': band['Title'],
                'link': band['Url'],
                'tag': 'hotsearch',
                'userName': 'toutiao',
            }
            hot_searches.append(item)
        except Exception as error:
            logging.error(error)
            continue

    return hot_searches

def main():
    res = fetch_hotsearch()
    print(res)
    
if __name__ == "__main__":
    main()
