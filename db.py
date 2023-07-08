from config import Config
import pymongo


class DB:
    client = pymongo.MongoClient(Config.mongo_url)
    db = client['sooshare']
    table = db['posts']
    def __init__(self, db_name='soo_share', table_name='posts') -> None:
        self.db = self.client[db_name]
        self.table = self.db[table_name]
        pass


    def exist_one(self, item):
        return self.table.find_one({'link': item['link']})

    def insert_one(self, item):
        self.table.insert_one(item)


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
