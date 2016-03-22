# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DownloadLinkItem(scrapy.Item):
    bulletin = scrapy.Field()
    product = scrapy.Field()
    url = scrapy.Field()
    files = scrapy.Field()
    msu_path = scrapy.Field()