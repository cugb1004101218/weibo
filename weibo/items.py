# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class User(scrapy.Item):
    # define the fields for your item here like:
    # 微博名称
    name = scrapy.Field()
    # user_id
    user_id = scrapy.Field()
    # 关注数
    follow_num = scrapy.Field()
    # 粉丝数
    fans_num = scrapy.Field()
    # 微博数
    weibo_num = scrapy.Field()

class Weibo(scrapy.Item):
    # user_id
    user_id = scrapy.Field()
    # weibo_id
    weibo_id = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 类型 转发、原创
    weibo_type = scrapy.Field()
    # 内容
    content = scrapy.Field()
