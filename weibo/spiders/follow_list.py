# -*- coding: utf-8 -*-
import scrapy
import urllib2
import time
import os


class FollowListSpider(scrapy.Spider):
  name = "follow_list"
  def __init__(self, user_id, follow_num=10, *args, **kwargs):
    super(FollowListSpider, self).__init__(*args, **kwargs)
    self.allowed_domains = ["www.weibo.cn"]
    url_list = []
    for i in range(1, int(follow_num) + 1):
      url_list.append("http://weibo.cn/" + str(user_id) + "/follow?page=" + str(i))
    self.start_urls = tuple(url_list)

  def start_requests(self):
    request_list = []
    cookies = {
      'SUHB':'0BLocYYzyZBSzZ',
      '_T_WM':'5fc7624dcb34415ad020fc52cef4aaed',
      'SUB':'_2A254J57nDeTxGeRG61QS-C_Fzz2IHXVb6yKvrDV6PUJbrdAKLVDukW030M9bliquIRovKJdQRPYhUyCLMQ..',
      'gsid_CTandWM':'4uUEf98d1Ey3z2DHQfU8RbM4dfb',
      'M_WEIBOCN_PARAMS':'from%3Dhome',
      '_T_WL':'1',
      '_WEIBO_UID':'2806381941',
    }
    for url in self.start_urls:
      request = scrapy.http.Request(url=url, cookies=cookies)
      request_list.append(request)
    return request_list

  def parse(self, response):
    profile_list = response.selector.xpath('//body/table')
    for profile in profile_list:
      temp = profile.xpath('tr/td/a')
      if len(temp) == 3:
        print temp[1].xpath('text()').extract()[0] + '\t' + temp[1].xpath('@href').extract()[0]

    time.sleep(1)

