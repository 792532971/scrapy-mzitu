# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import requests, os
base_path = 'D:\mzitu'


class MzituPipeline(object):

    def process_item(self, item, spider):
        # print(item['title'],item['img_url'])
        title = item['title']
        url = str(item['img_url'])
        print(url)
        if os.path.exists(os.path.join(base_path, item['title'])):
            pass
        else:
            os.makedirs(os.path.join(base_path, item['title']))
        dict = url.rsplit('/', maxsplit=1)
        file_name = os.path.join(base_path, title, dict[1])

        if os.path.exists(file_name):
            pass
        else:
            response = requests.get(url=url, headers={'Referer': 'http://www.mzitu.com/net/'})
            print('正在下载', title, '......')
            with open(file_name, 'wb') as f:
                f.write(response.content)
            print('下载完成.')
        raise DropItem()


class ImagespiderPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://www.mzitu.com/189982',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        print(item)

        for image_url in item['img_url']:
            self.default_headers['referer'] = image_url
            yield scrapy.Request(image_url,
                                 # meta={'item': item},
                                 headers=self.default_headers)

    # 如果重写这个函数,name为文件名下载
    # def file_path(self, request, response=None, info=None):
    #     # 提取url前面名称作为图片名。
    #     image_guid = request.url.split('/')[-1]  #得到图片后缀
    #     # 接收上面meta传递过来的图片名称
    #     item = request.meta['item']
    #     # 过滤windows字符串，不经过这么一个步骤，你会发现有乱码或无法下载
    #     # name = re.sub(r'[？\\*|“<>:/]', '', name)
    #     title = item['title']
    #     # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
    #     filename = u'{0}/{1}'.format(title, image_guid)
    #     return filename