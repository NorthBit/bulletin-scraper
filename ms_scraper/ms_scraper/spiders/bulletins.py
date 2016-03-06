# -*- coding: utf-8 -*-
import scrapy

from ..items import DownloadLinkItem


class BulletinsSpider(scrapy.Spider):
    name = "bulletins"
    start_urls = ['https://technet.microsoft.com/library/security/ms13-095']

    def parse(self, response):
        download_pages = {x for x in response.css('td a::attr("href")').extract() if 'familyid' in x.lower()}
        for download_page in download_pages:
            yield scrapy.Request(response.urljoin(download_page), self.resolve_download_page)

    def resolve_download_page(self, response):
        yield scrapy.Request(response.urljoin(response.url.replace('details.aspx', 'confirmation.aspx')),
                             self.download_updates)

    def download_updates(self, response):
        for link in response.css('td.file-link a::attr("href")').extract():
            item = DownloadLinkItem()
            item['link'] = link
            yield item
