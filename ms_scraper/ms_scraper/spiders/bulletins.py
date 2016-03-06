# -*- coding: utf-8 -*-
import scrapy

from ..items import DownloadLinkItem


class BulletinsSpider(scrapy.Spider):
    name = "bulletins"
    start_urls = ['https://technet.microsoft.com/library/security/ms13-095']

    def parse(self, response):
        for link in response.css('td a'):
            url = link.css('::attr(href)').extract_first()
            if 'familyid' not in url.lower():
                continue
            text = link.css('::text').extract_first()

            request = scrapy.Request(response.urljoin(url), self.resolve_download_page)
            request.meta['bulletin'] = response.url.rsplit('/', 1)[-1]
            request.meta['product'] = text
            yield request

    def resolve_download_page(self, response):
        yield scrapy.Request(response.urljoin(response.url.replace('details.aspx', 'confirmation.aspx')),
                             self.download_updates, meta=response.meta)

    def download_updates(self, response):
        for link in response.css('td.file-link a::attr("href")').extract():
            item = DownloadLinkItem()
            item['file_urls'] = [link]
            item['product'] = response.meta['product']
            item['bulletin'] = response.meta['bulletin']
            yield item
