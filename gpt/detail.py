import requests
import bs4
import json
import openai

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

def read_page(url: str):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    return soup


def fetch_detail(url: str):
        html = read_page(url)
        vacacy_text = html.find('div', class_='vacancy-text')
        ad = vacacy_text.find('div', class_='b')
        if ad:
            ad.extract()
        info = vacacy_text.text.replace("  ", "").replace("\n\n", "")
        return info
    
def fetch_detail(url: str):
    html = read_page(url)
    vacacy_text = html.find('div', class_='vacancy-text')
    ad = vacacy_text.find('div', class_='b')
    if ad:
        ad.extract()
    info = vacacy_text.text.replace("  ", "").replace("\n\n", "").strip()
    return info

class GPTHepler:
    def __init__(self, api_key) -> None:
        openai.api_key = api_key
        pass

    def get_prompt(self, info):
        info = '请帮助我对英文的岗位描述进行总结和关键词提炼，请保证 summary 足够完整并且适当分段，以及提炼的 tags 足够有代表性且不超过6个，提炼的 tag 应该具有代表性，例如当前岗位的特点。请确保你的 summary 和 tags 里的内容均为中文，并且以如下 JSON 形式回复 {"summary": "xxx", tags: ["x", "y", "z"]} 英文的岗位描述如下：' + info

        return {"role": "user", "content": info}


    def summrize_from_gpt(self, info):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[self.get_prompt(info)])
        return json.loads(response['choices'][0]['message']['content'])


def main():
    url = "https://uncareer.net/vacancy/intern-programme-management-temporary-595088"
    info = fetch_detail(url)
    print('info', info)
    # gpt_res = summrize_from_gpt(info)
    # print('response', gpt_res)
    # parsed_content = parse_gpt_response(gpt_res)
    # print(parsed_content)


if __name__ == "__main__":
    main()