import requests
import re
import logging
from bs4 import BeautifulSoup

def fetch_competitions():
    url = "https://m.saikr.com/vs/ajaxGetList"
    page = 1
    competitions = []
    while page < 10:
        try:
            response = requests.get(f'{url}?page={page}')
            if not response:
                break
            page += 1
            data = response.json()['data']['list']
            soup = BeautifulSoup(data, 'lxml')
            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                link = a_tag.get("href")
                title = a_tag.find("h3").get_text()
                time_divs = a_tag.find_all(class_="item-info item-time")
                sponsor_div = a_tag.find(class_="item-info item-sponsor")
                infos = [title]
                for div in time_divs + [sponsor_div]:
                    child_nodes = list(div.children)
                    tit = child_nodes[1].get_text().strip()
                    info = child_nodes[3].get_text().strip()
                    infos.append(tit + "：" + info)
                item = {
                    "content": "\n".join(infos),
                    "link": link,
                    "tag": "competition",
                    "userName": "saikr"
                }
                competitions.append(item)
        except Exception as error:
            logging.error(error)
            continue

    return competitions[::-1]


if __name__ == "__main__":
    # items = fetch_competitions()
    # print(items)
    response = requests.get("https://m.saikr.com/vs/ajaxGetList?page=100")
    print(response)
