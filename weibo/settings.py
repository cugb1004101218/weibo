# -*- coding: utf-8 -*-

# Scrapy settings for weibo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'
CONCURRENT_REQUESTS_PER_DOMAIN = 1

ITEM_PIPELINES = {
    'weibo.pipelines.WeiboPipeline': 1,
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36'

# 抓取延迟
DOWNLOAD_DELAY = 1

cookies = {
    '_T_WM':'00f3d7e52fbb96b4c9dde5234b6aba51',
    'SUB':'_2A256D-QLDeRxGeRG61QS-C_Fzz2IHXVZ84xDrDV6PUJbrdAKLVHjkW1LHesu9VprumlGR7enK7bPU6sDBL1jCw..',
    'gsid_CTandWM':'4u9R33741UirXiAEKNJPRbM4dfb',
    '_T_WL':'1',
    '_WEIBO_UID':'2806381941',
}
