from config import Config
from db import DB
from threading import Timer
from datetime import datetime
import spiders.weibo as spiders


class Updater:
    def __init__(self) -> None:
        self.db = DB()
        self.interval = 60

    def update_hotsearch(self):
        print("Update hotsearch at:" + str(datetime.now()))
        hot_searches = spiders.fetch_hotsearch(Config.weibo_cookie)
        for item in hot_searches:
            if self.db.find_one(item):
                continue
            self.db.insert_one(item)
        Timer(self.interval, self.update_hotsearch).start()


def main():
    updater = Updater()
    updater.update_hotsearch()


if __name__ == "__main__":
    main()
