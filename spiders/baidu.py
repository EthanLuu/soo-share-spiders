from datetime import datetime
import requests
import pytz
from bs4 import BeautifulSoup
import logging


def fetch_hotsearch():
    url = "https://top.baidu.com/board?tab=realtime"
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')
    container = soup.find("main")
    title_elements = container.find_all(class_="c-single-text-ellipsis")
    res = []
    for title_element in title_elements:
        title = title_element.string.strip()
        link_element = title_element.parent
        link = link_element.get('href')
        content_element = link_element.parent.find_all("div")[2]
        content = content_element.get_text()
        if not content:
            content = ""
        try:
            item = {
                'content': "#%s# %s" % (title.replace("#", ""), content.replace(" 查看更多> ", "")),
                'link': link,
                'tag': 'hotsearch',
                'userName': 'baidu',
                'date': datetime.now(pytz.timezone('Asia/Shanghai'))
            }
            res.append(item)
        except Exception as error:
            logging.error(error)
            continue
    return res


if __name__ == "__main__":
    res = fetch_hotsearch()
    print(res)