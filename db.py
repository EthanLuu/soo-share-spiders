from config import Config
import pymongo


class DB:
    client = pymongo.MongoClient(Config.mongo_url)
    db = client['sooshare']
    posts = db['posts']

    def find_one(self, item):
        return self.posts.find_one({'link': item['link']})

    def insert_one(self, item):
        self.posts.insert_one(item)
