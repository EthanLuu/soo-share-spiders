import requests
import bs4
import re
from datetime import datetime

def parse_date(s: str):
    date_pattern = r"(\d{2}\s\w+\s\d{4})"
    matches = re.findall(date_pattern, s)
    if len(matches) == 0:
        return None
    date_string = matches[0]
    date_format = "%d %B %Y"
    date = datetime.strptime(date_string, date_format)
    return date


def parse_elements(elements: list):
    base_url = "https://uncareer.net"
    items = []
    for element in elements:
        link = base_url + element.find('a').get('href')
        title = element.find('a').text
        split_title = title.split(", ")
        desc = ", ".join(split_title[:-1])
        city = split_title[-1]
        p_elements = element.find_all('p')
        start_date = ""
        end_date = ""
        if len(p_elements) >= 2:
            start_date = p_elements[1].text
        if len(p_elements) >= 3:
            end_date = p_elements[2].text
        items.append({
            'link': link,
            'title': desc,
            'city': city,
            'start_date': parse_date(start_date),
            'end_date': parse_date(end_date)
        })
    return items

def read_page(url: str):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup


def insert_all(items):
    pass

def fetch_all():
    base_url = 'https://uncareer.net/tag/internship'
    page = 1
    items_all = []
    while True:
        if page > 50:
            break
        cur_url = f'{base_url}?page={page}'
        print(f'Fetching {cur_url}')
        html = read_page(url=cur_url)
        elements = html.find_all('div', class_='vacancy')
        if len(elements) == 0:
            break
        items = parse_elements(elements)
        items_all.extend(items)
        page += 1
    return items_all
    
def main():
    fetch_all()
    print(parse_date(""))
    
if __name__ == "__main__":
    main()