# -*- coding: utf-8 -*-
import scrapy
import urllib2
import time
import os
from weibo.items import Weibo
from weibo.settings import cookies


class WeiboListSpider(scrapy.Spider):
    name = "weibo_list"
    def __init__(self, user_id, *args, **kwargs):
        super(WeiboListSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["www.weibo.cn"]
        url_list = []
        url_list.append("http://weibo.cn/" + str(user_id) + "?page=1")
        self.start_urls = tuple(url_list)
        self.user_id = user_id
        self.cookies = cookies

    def start_requests(self):
        request_list = []
        for url in self.start_urls:
            request = scrapy.http.Request(url=url, cookies=self.cookies)
            request_list.append(request)
        return request_list

    def parse(self, response):
        page_num = int(response.selector.xpath('//*[@id="pagelist"]/form/div/input[1]/@value').extract()[0])
        for i in range(1, page_num + 1):
            url = "http://weibo.cn/" + str(self.user_id) + "?page=" + str(i)
            yield scrapy.http.Request(url=url,
                                      cookies=self.cookies,
                                      callback=lambda response,
                                      page=i: self.crawl_weibo(response, page), dont_filter=True)

    def crawl_weibo(self, response, page):
        profile_list = response.selector.xpath('//div[@class="c"]')

        for profile in profile_list:
            weibo_item = Weibo()
            weibo_item["user_id"] = self.user_id
            try:
                weibo_item["weibo_id"] = profile.xpath('@id').extract()[0]
            except:
                continue
            source = profile.xpath('div/span[@class="cmt"]//text()').extract()
            # 原创
            if len(source) == 0:
                weibo_item["weibo_type"] = "repost"
                weibo_item["weibo_type"] = "original"
                weibo_item["author"] = self.user_id
            else:
                weibo_item["weibo_type"] = "repost"
                try:
                    weibo_item["author"] = profile.xpath('div/span[@class="cmt"]/a/@href').extract()[0].strip().split('/')[-1]
                except:
                    continue
            weibo = profile.xpath('div/span[@class="ctt"]//text()').extract()
            weibo_item["content"] = "".join(weibo)

            ## user_id
            #print weibo_item["user_id"]
            ## weibo_id
            #print weibo_item["weibo_id"]
            ## 作者
            #print weibo_item["author"]
            ## 类型 转发、原创
            #print weibo_item["weibo_type"]
            ## 内容
            #print weibo_item["content"]
            yield weibo_item
