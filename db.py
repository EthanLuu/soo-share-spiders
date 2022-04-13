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
        if db.posts.count_documents({"content": post['content']}) == 1:
            continue
        db.posts.delete_many({"content": post['content']})
        print(post['content'])


if __name__ == "__main__":
    main()
