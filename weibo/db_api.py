# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import sys
import unittest
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/home/cugbacm/weibo/weibo/weibo.config')
db_engine = config.get("db", "db_engine")
db_ip = config.get("db", "db_ip")
db_port = config.getint("db", "db_port")
db_name = config.get("db", "db_name")
weibo_item_table_name = config.get("db", "weibo_item_table_name")
user_table_name = config.get("db", "user_table_name")

class DBAPI(object):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        self.db_engine = db_engine
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_name = db_name
        self.table_name = table_name
        if self.db_engine == "mongo":
            self.conn = pymongo.MongoClient(host=self.db_ip, port=self.db_port)
            self.db = self.conn[self.db_name]
            self.table = self.db[self.table_name]

    def get_one(self, query):
        return self.table.find_one(query, projection={"_id": False})

    def get_all(self, query):
        return self.table.find(query)

    def add(self, kv_dict):
        return self.table.insert(kv_dict)

    def delete(self, query):
        return self.table.delete_many(query)

    def check_exist(self, query):
        return self.get_one(query) != None

    # 如果没有 会新建
    def update(self, query, kv_dict):
        ret = self.table.update_many(
            query,
            {
                "$set": kv_dict,
            }
        )
        if not ret.matched_count or ret.matched_count == 0:
            self.add(kv_dict)
        elif ret.matched_count and ret.matched_count > 1:
            self.delete(query)
            self.add(kv_dict)

class WeiboItemDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(WeiboItemDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_weibo_item(self, weibo_id, kv_dict):
        if self.check_exist({"weibo_id": weibo_id}):
            return
        self.add(kv_dict)

    def get_weibo_item(self, weibo_id):
        query = {}
        query["weibo_id"] = weibo_id
        return self.get_one(query)

class UserDBAPI(DBAPI):
    def __init__(self, db_engine, db_ip, db_port, db_name, table_name):
        super(UserDBAPI, self).__init__(db_engine, db_ip, db_port, db_name, table_name)

    def add_user(self, user_id, kv_dict):
        query = {"user_id": user_id}
        self.update(query, kv_dict)

    def get_user(self, user_id):
        query = {"user_id": user_id}
        return self.get_one(query)

class DBAPITest(unittest.TestCase):
    def setUp(self):
        self.db_api = DBAPI(db_engine,
                            db_ip,
                            db_port,
                            "test",
                            "test_table")

    def test(self):
        db_api = self.db_api
        db_api.add({"url": "test_url", "k": "v"})
        self.assertEqual(db_api.get_one({"url": "test_url"})["k"], "v")

        db_api.update({"url": "test_url"}, {"url_update": "url_update"})
        ob = db_api.get_one({"url": "test_url"})
        self.assertEqual(ob["url_update"], "url_update")

        db_api.delete({"url": "test_url"})
        self.assertEqual(db_api.get_one({"url": "test_url"}), None)

class WeiboItemDBAPITest(unittest.TestCase):
    def setUp(self):
        self.db_api = WeiboItemDBAPI(db_engine,
                                     db_ip,
                                     db_port,
                                     "test",
                                     "test_table")

    def test(self):
        db_api = self.db_api
        weibo_item = {}
        # user_id
        weibo_item["user_id"] = "test_id"
        # weibo_id
        weibo_item["weibo_id"] = "weibo_id"
        # 作者
        weibo_item["author"] = "author"
        # 类型 转发、原创
        weibo_item["weibo_type"] = "weibo_type"
        # 内容
        weibo_item["content"] = "content"
        db_api.add_weibo_item("weibo_id", weibo_item)
        ret = db_api.get_weibo_item("weibo_id")
        self.assertEqual(ret["user_id"]   , weibo_item["user_id"])
        self.assertEqual(ret["weibo_id"]  , weibo_item["weibo_id"])
        self.assertEqual(ret["author"]    , weibo_item["author"])
        self.assertEqual(ret["weibo_type"], weibo_item["weibo_type"])
        self.assertEqual(ret["content"]   , weibo_item["content"])
        db_api.delete({"weibo_id": "weibo_id"})

class UserDBAPITest(unittest.TestCase):
    def setUp(self):
        self.db_api = UserDBAPI(db_engine,
                                db_ip,
                                db_port,
                                "test",
                                "test_table")

    def test(self):
        db_api = self.db_api
        user = {}
        user["user_id"] = "12345678"
        user["name"] = "name"
        db_api.add_user(user["user_id"], user)
        ret = db_api.get_user(user["user_id"])
        self.assertEqual(ret["user_id"], user["user_id"])
        self.assertEqual(ret["name"], user["name"])
        db_api.delete({"user_id": "user_id"})

# 微博DBAPI
weibo_item_db_api = WeiboItemDBAPI(db_engine,
                                   db_ip,
                                   db_port,
                                   db_name,
                                   weibo_item_table_name)

# 微博用户DBAPI
user_db_api = UserDBAPI(db_engine,
                        db_ip,
                        db_port,
                        db_name,
                        user_table_name)

if __name__ == '__main__':
    unittest.main()
