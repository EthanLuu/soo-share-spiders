from config import Config
from db import DB
import os
from threading import Timer
from datetime import datetime
import spiders.weibo as weibo
import spiders.baidu as baidu
import spiders.saikr as sakir
import logging
import jieba
import pytz


class Updater:
    def __init__(self) -> None:
        self.db = DB()
        self.interval = 60
        self.init_log()
        self.update_log_config()

    def init_log(self):
        self.log_base_path = "log"
        if not os.path.exists(self.log_base_path):
            os.makedirs(self.log_base_path)
        self.update_log_config()

    def run(self):
        self.update_log_config()
        self.update_baidu_hotsearch()
        self.update_weibo_hotsearch()
        self.update_sakir_competition()
        Timer(self.interval, self.run).start()

    def add_date_and_keywords(self, item):
        item['date'] = datetime.now(pytz.timezone('Asia/Shanghai')),
        item['keywords'] = " ".join(jieba.cut(item['content']))
        return item

    def update_log_config(self):
        filename = self.log_base_path + "/" + \
            datetime.now().strftime("%Y-%m-%d") + ".log"
        logging.basicConfig(filename=filename,
                            encoding='utf-8', level=logging.INFO)

    def update_sakir_competition(self):
        logging.info("Update sakir hot search at: " + str(datetime.now()))
        try:
            items = sakir.fetch_competitions()
            for item in items:
                if self.db.find_one(item):
                    continue
                item = self.add_date_and_keywords(item)
                self.db.insert_one(item)
                logging.info(item)
        except Exception as e:
            logging.error(e)

    def update_weibo_hotsearch(self):
        logging.info("Update weibo hot search at: " + str(datetime.now()))
        try:
            hot_searches = weibo.fetch_hotsearch(Config.weibo_cookie)
            for item in hot_searches:
                if self.db.find_one(item):
                    continue
                item = self.add_date_and_keywords(item)
                self.db.insert_one(item)
                logging.info(item)
        except Exception as e:
            logging.error(e)

    def update_baidu_hotsearch(self):
        logging.info("Update baidu hot search at: " + str(datetime.now()))
        try:
            hot_searches = baidu.fetch_hotsearch()
        except Exception as e:
            logging.error(e)
            for item in hot_searches:
                if self.db.find_one(item):
                    continue
                item = self.add_date_and_keywords(item)
                self.db.insert_one(item)
                logging.info(item)


def main():
    updater = Updater()
    updater.run()


if __name__ == "__main__":
    main()
