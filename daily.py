from config import Config
from db import DB
import os
from datetime import datetime
import spiders.weibo as weibo
import spiders.baidu as baidu
import spiders.saikr as sakir
import spiders.toutiao as toutiao
import spiders.un_intern as un
import logging
import jieba
import pytz


class Updater:
    def __init__(self) -> None:
        self.db = DB('utils', 'un_intern')
        self.init_log()
        self.update_log_config()

    def init_log(self):
        self.log_base_path = "log"
        if not os.path.exists(self.log_base_path):
            os.makedirs(self.log_base_path)
        self.update_log_config()

    def run(self):
        self.update_log_config()
        self.update_un_intern()

    def update_log_config(self):
        filename = self.log_base_path + "/" + \
            datetime.now().strftime("%Y-%m-%d") + ".log"
        logging.basicConfig(filename=filename, level=logging.INFO)

    def fetch_and_insert(self, fetch):
        try:
            items = fetch()
            for item in items:
                if self.db.exist_one(item):
                    continue
                self.db.insert_one(item)
                logging.info(item)
        except Exception as e:
            logging.error(e)

    def update_un_intern(self):
        logging.info("Update un intern at: " + str(datetime.now()))
        self.fetch_and_insert(un.fetch_all)


def main():
    updater = Updater()
    updater.run()


if __name__ == "__main__":
    main()
