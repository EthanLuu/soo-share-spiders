import requests
import bs4
import json


def read_page(url: str):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup


def fetch_detail(url):
    html = read_page(url)
    vacacy_text = html.find('div', class_='vacancy-text')
    ad = vacacy_text.find('div', class_='b')
    if ad:
        ad.extract()
    info = vacacy_text.text.replace("  ", "").replace("\n\n", "")
    return info


def get_prompt(info):
    info = 'Give me the result in the form of {"summary": "xxx", tags: ["x", "y", "z"]} 请确保你的回答是中文，并且保证 summary 足够完整，以及提炼的 tags 足够有代表性。Here is the job descrption: ' + info

    return str([{"role": "user", "content": info}])


def summrize_from_gpt(info):
    url = "https://gpt-api.ethanloo.cn/ask"
    response = requests.post(url,
                             params={
                                 'site': 'vita',
                                 "prompt": get_prompt(info)
                             })
    content = response.json()['content']
    return content


def parse_gpt_response(response):
    return json.loads(response)


def main():
    url = "https://uncareer.net/vacancy/mission-france-stage-assistante-logistique-et-finance-hf-toulouse-602418"
    info = fetch_detail(url)
    gpt_res = summrize_from_gpt(info)
    print(parse_gpt_response(gpt_res))


if __name__ == "__main__":
    main()