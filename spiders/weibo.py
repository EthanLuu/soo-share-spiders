from datetime import datetime
import requests
import re
import pytz


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
            item = {
                'content': pattern.sub('', band['mblog']['text']),
                'link': "https://s.weibo.com/weibo?q=%23" + band['note'] + "%23",
                'tag': 'hotsearch',
                'userName': 'xinlang',
                'date': datetime.now(pytz.timezone('Asia/Shanghai'))
            }
            hot_searches.append(item)
        except:
            continue

    return hot_searches
