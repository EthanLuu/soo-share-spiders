from db import DB
from gpt.detail import fetch_detail, summrize_from_gpt
import json


class Updater:

    def __init__(self) -> None:
        self.jobs_db = DB('utils', 'jobs')
        self.details_db = DB('utils', 'details')

    def check_exist(self, jobId):
        return self.details_db.table.find_one({'jobId': jobId}) is not None

    def parse_all(self):
        jobs = self.jobs_db.table.find({})
        for job in jobs:
            jobId = job['_id']
            if self.check_exist(jobId):
                continue
            link = job['link']
            try:
                detail_str = fetch_detail(link)
                gpt_response = summrize_from_gpt(detail_str)
                detail_obj = json.loads(gpt_response)
                self.details_db.insert_one({
                    'jobId':
                    jobId,
                    'raw':
                    detail_str,
                    'summary':
                    detail_obj.get('summary', ''),  # 如果没有summary字段，返回空字符串
                    'tags':
                    detail_obj.get('tags', []),  # 如果没有tags字段，返回空列表
                })
                print('raw', detail_str)
                print('gpt', detail_obj)
            except json.JSONDecodeError as e:
                print(f'Error decoding JSON for jobId {jobId}: {e}')
                continue
            except Exception as e:
                print(f'Error for jobId {jobId}: {e}')
                continue

    def run(self):
        self.parse_all()


def main():
    updater = Updater()
    updater.run()


if __name__ == "__main__":
    main()
