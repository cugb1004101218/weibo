# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from db_api import weibo_item_db_api
from db_api import user_db_api

class WeiboPipeline(object):
    def process_item(self, item, spider):
        if spider.name not in ["weibo_list", "search_user_id"]:
            return item
        if str(item.__class__) == "<class 'weibo.items.Weibo'>":
            weibo_item_db_api.add_weibo_item(item["weibo_id"], dict(item))
        elif str(item.__class__) == "<class 'weibo.items.User'>":
            print "fuck"
            user_db_api.add_user(item["user_id"], dict(item))
        return item
