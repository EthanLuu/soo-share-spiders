import requests
import bs4
import re


def read_page(url: str):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup

def fetch_detail(url):
    html = read_page(url)
    info = html.find('div', class_='vacancy-text').text.replace("  ", "").replace("\n", "")
    return info

def get_prompt(info):
    info = "I hope you can help me summarize the job description and translate it into chinese. Here is the job descrption: " + info
    
    return str([{"role": "user", "content": info}])

def summrize_from_gpt(info):
    url = "https://gpt-api.ethanloo.cn/ask"
    response = requests.post(url, params={'site': 'vita', "prompt": get_prompt(info)})
    content = response.json()['content']
    return content

def main():
    url = "https://uncareer.net/vacancy/associate-it-officer-knowledge-management-230232-602170"
    info = fetch_detail(url)
    gpt_info = summrize_from_gpt(info)
    print(gpt_info)
    
if __name__ == "__main__":
    main()