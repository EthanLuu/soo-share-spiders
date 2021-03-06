import requests
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
        content = "#%s# %s" % (title.replace(
            "#", ""), content_element.get_text().replace(" 查看更多> ", ""))
        if not content:
            content = ""
        try:
            item = {
                'content': content,
                'link': link,
                'tag': 'hotsearch',
                'userName': 'baidu',
            }
            res.append(item)
        except Exception as error:
            logging.error(error)
            continue
    return res


if __name__ == "__main__":
    res = fetch_hotsearch()
    print(res)
