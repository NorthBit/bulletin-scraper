import scrapy

import scrapy.pipelines.files

# From Monthly Update
# print set(response.css('td[data-th="Bulletin ID"] a::attr("href")').extract())

class BulletinSpider(scrapy.Spider):
    name = 'BulletinSpider'
    start_urls = ['https://technet.microsoft.com/library/security/ms13-095']

    def parse(self, response):
        download_pages = {x for x in response.css('td a::attr("href")').extract() if 'familyid' in x.lower()}
        for download_page in download_pages:
            yield scrapy.Request(response.urljoin(download_page), self.resolve_download_page)

    def resolve_download_page(self, response):
        yield scrapy.Request(response.urljoin(response.url.replace('details.aspx','confirmation.aspx')), self.download_updates)

    def download_updates(self, response):
        print response.css('td.file-link a::attr("href")').extract()




from scrapy.exceptions import DropItem

class PricePipeline(object):

    vat_factor = 1.15

    def process_item(self, item, spider):
        if item['price']:
            if item['price_excludes_vat']:
                item['price'] = item['price'] * self.vat_factor
            return item
        else:
            raise DropItem("Missing price in %s" % item)


#
# {x for x in response.css('td a::attr("href")').extract() if 'familyid' in x.lower()}
#
# response.url.replace('details.aspx','confirmation.aspx')
#
# response.css('td.file-link a::attr("href")').extract()
