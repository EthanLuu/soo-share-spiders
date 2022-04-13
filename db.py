from config import Config
import pymongo


class DB:
    client = pymongo.MongoClient(Config.mongo_url)
    db = client['sooshare']
    posts = db['posts']

    def exist_one(self, item):
        return self.posts.find_one({'link': item['link']}) or self.posts.find_one({'content': item['content']})

    def insert_one(self, item):
        self.posts.insert_one(item)


def main():
    db = DB()
    posts = db.posts.find({})
    for post in posts:
        print(post['date'])
        if type(post['date']) == type([]):
            db.posts.find_one_and_update({"_id": post['_id']}, {
                '$set': {
                    "date": post['date'][0]
                }
            })

        # break
        # db.posts.update_one({"content": post['content']})
        # print(post['content'])


if __name__ == "__main__":
    main()
