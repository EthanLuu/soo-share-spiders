from config import Config
from db import DB
from threading import Timer
from datetime import datetime
import spiders.weibo as weibo
import spiders.baidu as baidu



class Updater:
    def __init__(self) -> None:
        self.db = DB()
        self.interval = 60

    def update_weibo_hotsearch(self):
        print("Update weibo hot search at: " + str(datetime.now()))
        hot_searches = weibo.fetch_hotsearch(Config.weibo_cookie)
        for item in hot_searches:
            if self.db.find_one(item):
                continue
            self.db.insert_one(item)
            print(item)
        Timer(self.interval, self.update_weibo_hotsearch).start()

    def update_baidu_hotsearch(self):
        print("Update baidu hot search at: " + str(datetime.now()))
        hot_searches = baidu.fetch_hotsearch()
        for item in hot_searches:
            if self.db.find_one(item):
                continue
            self.db.insert_one(item)
            print(item)
        Timer(self.interval, self.update_baidu_hotsearch).start()


def main():
    updater = Updater()
    updater.update_weibo_hotsearch()
    updater.update_baidu_hotsearch()


if __name__ == "__main__":
    main()
