# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import subprocess

import scrapy.pipelines.files
from scrapy.exceptions import DropItem
import os
import scrapy
import errno

SYMCHK_PATH = r'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\symchk.exe'
SYM_PATH = r'SRV*c:\temp\symbols*https://msdl.microsoft.com/download/symbols'


def expand(source, dest, filter_='*'):
    subprocess.call(['expand', '-F:{}'.format(filter_), source, dest])

def delete(path):
    subprocess.call(['del', '/Q', path], shell=True)

def symchk(path, symchk_path=None, sym_path=None, output_dir=None):
    if symchk_path is None:
        symchk_path = SYMCHK_PATH
    if sym_path is None:
        sym_path = SYM_PATH

    output_dir_args = []
    if output_dir is not None:
        output_dir_args = ['/oc', output_dir]

    subprocess.call([symchk_path, '/r', path, '/s', sym_path, ] + output_dir_args)


class MsuDownloadPipeline(scrapy.pipelines.files.FilesPipeline):
    def get_media_requests(self, item, info):
        request = scrapy.Request(item['url'])
        request.meta['bulletin'] = item['bulletin']
        yield request

    def item_completed(self, results, item, info):
        file_paths = (result['path'] for ok, result in results if ok)
        msu_paths = [path for path in file_paths if path.lower().endswith('.msu')]
        if not msu_paths:
            raise DropItem("Item is not an MSU")
        item['msu_path'] = msu_paths[0]
        return item

    def file_path(self, request, response=None, info=None):
        bulletin = request.meta['bulletin'].upper()
        path = os.path.join(bulletin, request.url.rsplit('/', 1)[-1])
        return path


class MsuExtractPipeline(object):
    def process_item(self, item, spider):
        msu_path = os.path.join(spider.settings['FILES_STORE'], item['msu_path'])
        msu_dir = os.path.dirname(msu_path)
        msu_name = item['url'].rsplit('/', 1)[-1].rsplit('.', 1)[0]
        extract_dir = os.path.join(msu_dir, msu_name)
        try:
            os.mkdir(extract_dir)
        except WindowsError as e:
            if e.errno != errno.EEXIST:
                raise

        extract_cab = '{}.cab'.format(msu_name)
        expand(msu_path, extract_dir, extract_cab)
        filter_ = spider.settings.get('EXTRACT_FILTER', None)
        expand(os.path.join(extract_dir, extract_cab), extract_dir, filter_=filter_)

        if spider.settings.get('DELETE_RUBBISH', False):
            # Delete all files that are not in directories. This includes a lot of rubbish files, as well as the
            # original `.cab` file.
            delete(os.path.join(extract_dir, '*'))

        if not spider.settings.get('DONT_DOWNLOAD_SYMBOLS', False):
            self.download_symbols(extract_dir, spider)

        if spider.settings.get('DELETE_MSU_FILES', False):
            try:
                os.unlink(msu_path)
            except WindowsError:
                pass

        if spider.settings.get('DELETE_EMPTY_DIRS', True):
            drop_item = False
            if not os.listdir(extract_dir):
                os.rmdir(extract_dir)
                drop_item = True

            if not os.listdir(msu_dir):
                os.rmdir(msu_dir)

            if drop_item:
                raise DropItem('No item found.')

        return item

    def download_symbols(self, extract_dir, spider):
        symchk_path = spider.settings.get('SYMCHK_PATH', None)
        sym_path = spider.settings.get('SYM_PATH', None)
        output_dir = spider.settings.get('DOWNLOAD_SYMBOLS_TO', None)
        symchk(extract_dir, symchk_path=symchk_path, sym_path=sym_path, output_dir=output_dir)
