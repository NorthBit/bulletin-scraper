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


PLATFORM_LIST = None
EXTRACT_FILTER = 'ntdll.dll'

## Set `DONT_DOWNLOAD_SYMBOLS` to `True` to prevent downloading symbols.
DONT_DOWNLOAD_SYMBOLS = False

SYMCHK_PATH = r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe'
SYM_PATH = r'SRV*c:\temp\symbols*https://msdl.microsoft.com/download/symbols'

# Set a path to download symbols to. Otherwise - uses what is in `SYM_PATH`.
DOWNLOAD_SYMBOLS_TO = r'c:\temp\syms'

# Delete `.msu` files after extraction
DELETE_MSU_FILES = True

# Delete rubbish files (the `.msu` files are full of them!)
DELETE_RUBBISH = True

# Delete empty directories
DELETE_EMPTY_DIRS = True

ITEM_PIPELINES = {
    'ms_scraper.pipelines.MsuDownloadPipeline' : 300,
    'ms_scraper.pipelines.MsuExtractPipeline' : 500,
}
FILES_STORE = r'C:\Temp\scraped'