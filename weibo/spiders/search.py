# -*- coding: utf-8 -*-
import scrapy
import urllib2
import time
import os

from weibo.settings import cookies
from weibo.items import User

class SearchSpider(scrapy.Spider):
    name = "search_user_id"
    def __init__(self, user_name="杨幂", *args, **kwargs):
        super(SearchSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["www.weibo.cn"]
        self.user_name = user_name
        self.cookies = cookies

    def start_requests(self):
        return [scrapy.http.Request(url="http://weibo.cn/search/?pos=search&keyword=" + self.user_name + "&suser=找人", cookies = self.cookies, callback = self.search)]

    def search(self, response):
        user = response.selector.xpath('//body/table/tr')
        url = "http://www.weibo.cn"
        if len(user) > 0:
            user_id = user[0].xpath('td/a/@href').extract()
            if len(user_id) > 0:
                url += user_id[0]
        user_id = url.strip().split('?')[0].split('/')[-1]
        user = User()
        user["user_id"] = user_id
        user["name"] = self.user_name
        yield user
