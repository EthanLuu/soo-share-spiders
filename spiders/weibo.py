from datetime import datetime
import requests
import re
import pytz
import logging
import jieba

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
            content =  pattern.sub('', band['mblog']['text'])
            item = {
                'content': pattern.sub('', band['mblog']['text']),
                'link': "https://s.weibo.com/weibo?q=%23" + band['note'] + "%23",
                'tag': 'hotsearch',
                'userName': 'xinlang',
                'date': datetime.now(pytz.timezone('Asia/Shanghai')),
                'keywords': " ".join(jieba.cut(content))
            }
            hot_searches.append(item)
        except Exception as error:
            logging.error(error)
            continue

    return hot_searches
