import requests
import re
import logging

def fetch_hotsearch(cookie):
    url = "https://weibo.com/ajax/statuses/hot_band"
    headers = {"cookie": cookie}
    response = requests.get(url, headers=headers)
    data = response.json()['data']
    band_list = data['band_list']
    hot_searches = []
    pattern = re.compile(r'<[^>]+>', re.S)
    

    for band in band_list:
        try:
            content = pattern.sub('', band['mblog']['text'])
            link = "https://s.weibo.com/weibo?q=%23" + band['note'] + "%23"
            if "此微博已被删除" in content: continue
            item = {
                'content': content,
                'link': link,
                'tag': 'hotsearch',
                'userName': 'xinlang',
            }
            hot_searches.append(item)
        except Exception as error:
            logging.error(error)
            continue

    return hot_searches
