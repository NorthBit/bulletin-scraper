# -*- coding: utf-8 -*-
import scrapy


class BulletinsSpider(scrapy.Spider):
    name = "bulletins"
    allowed_domains = ["https://technet.microsoft.com/library/security/ms13-095"]
    start_urls = (
        'http://www.https://technet.microsoft.com/library/security/ms13-095/',
    )

    def parse(self, response):
        pass
