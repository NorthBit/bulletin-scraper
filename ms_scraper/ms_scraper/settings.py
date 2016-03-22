# -*- coding: utf-8 -*-

# Scrapy settings for ms_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ms_scraper'

SPIDER_MODULES = ['ms_scraper.spiders']
NEWSPIDER_MODULE = 'ms_scraper.spiders'


# List of products to download, based on the names on the bulletin pages.
PRODUCT_LIST = []

# Set a filter for cab extraction. Note that it only affects the extraction.
EXTRACT_FILTER = None

## Set `DONT_DOWNLOAD_SYMBOLS` to `True` to prevent downloading symbols.
DONT_DOWNLOAD_SYMBOLS = False

SYMCHK_PATH = r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe'
SYM_PATH = r'SRV*C:\temp\symbols*https://msdl.microsoft.com/download/symbols'

# Delete `.msu` files after extraction
DELETE_MSU_FILES = False

# Delete rubbish files (the `.msu` files are full of them!)
DELETE_RUBBISH = True


ITEM_PIPELINES = {
    'ms_scraper.pipelines.MsuDownloadPipeline' : 300,
    'ms_scraper.pipelines.MsuExtractPipeline' : 500,
}
FILES_STORE = r'.\scraped'