from config import Config
from db import DB
import os
from threading import Timer
from datetime import datetime
import spiders.weibo as weibo
import spiders.baidu as baidu
import logging


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
        Timer(self.interval, self.run).start()
        
    def update_log_config(self):
        filename = self.log_base_path + "/" + datetime.now().strftime("%Y-%m-%d") + ".log"
        logging.basicConfig(filename=filename, encoding='utf-8', level=logging.INFO)

    def update_weibo_hotsearch(self):
        logging.info("Update weibo hot search at: " + str(datetime.now()))
        hot_searches = weibo.fetch_hotsearch(Config.weibo_cookie)
        for item in hot_searches:
            if self.db.find_one(item):
                continue
            self.db.insert_one(item)
            logging.info(item)

    def update_baidu_hotsearch(self):
        logging.info("Update baidu hot search at: " + str(datetime.now()))
        hot_searches = baidu.fetch_hotsearch()
        for item in hot_searches:
            if self.db.find_one(item):
                continue
            self.db.insert_one(item)
            logging.info(item)


def main():
    updater = Updater()
    updater.run()


if __name__ == "__main__":
    main()
