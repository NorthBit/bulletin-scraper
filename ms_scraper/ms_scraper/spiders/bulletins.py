# -*- coding: utf-8 -*-
import scrapy

from ..items import DownloadLinkItem


class BulletinsSpider(scrapy.Spider):
    name = "bulletins"
    start_urls = ['https://technet.microsoft.com/en-us/library/security/dn631937.aspx']

    def parse(self, response):
        for link in response.xpath('//a[string-length(@title)=4]'):
            title = link.xpath('@title').extract_first()
            try:
                year = int(title)
            except ValueError:
                # We need only the years!
                continue

            url = link.xpath('@href').extract_first()

            yield scrapy.Request(response.urljoin(url), self.parse_bulletin_table)

    def parse_bulletin_table(self, response):
        for url in response.xpath('//td/p/a/@href').extract():
            yield scrapy.Request(response.urljoin(url), self.parse_bulletin_page)

    def parse_bulletin_page(self, response):
        visited_urls = set()
        for link in response.css('td a'):
            url = link.css('::attr(href)').extract_first()
            if url in visited_urls:
                continue
            visited_urls.add(url)
            if 'familyid' not in url.lower():
                continue
            text = link.css('::text').extract_first()

            if text not in self.settings.get['PRODUCT_LIST', []]:
                continue

            request = scrapy.Request(response.urljoin(url), self.resolve_download_page)
            request.meta['bulletin'] = response.url.rsplit('/', 1)[-1].rsplit('.', 1)[0]
            request.meta['product'] = text
            yield request

    def resolve_download_page(self, response):
        yield scrapy.Request(response.urljoin(response.url.replace('details.aspx', 'confirmation.aspx')),
                             self.download_updates, meta=response.meta)

    def download_updates(self, response):
        for url in response.css('td.file-link a::attr("href")').extract():
            item = DownloadLinkItem()
            item['url'] = url
            item['product'] = response.meta['product']
            item['bulletin'] = response.meta['bulletin']
            yield item
