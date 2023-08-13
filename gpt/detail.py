import requests
import bs4
import json
import g4f

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}


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
    info = '请帮助我对英文的岗位描述进行总结和分析，请保证 summary 足够完整并且适当分段，以及提炼的 tags 足够有代表性且不超过6个。请确保你的 summary 和 tags 里的内容均为中文，并且以如下 JSON 形式回复 {"summary": "xxx", tags: ["x", "y", "z"]} 英文的岗位描述如下：' + info

    return {"role": "user", "content": info}


def summrize_from_gpt(info):
    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.GetGpt, messages=[
                                     get_prompt(info)], stream=False)
    return response


def parse_gpt_response(response):
    return json.loads(response)


def main():
    url = "https://uncareer.net/vacancy/internship-corporate-performance-analysis-and-reporting-hq-rome-italy-595313"
    info = fetch_detail(url)
    print('info', info)
    gpt_res = summrize_from_gpt(info)
    print('response', gpt_res)
    print(parse_gpt_response(gpt_res))


if __name__ == "__main__":
    main()