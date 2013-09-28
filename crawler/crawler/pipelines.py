# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
from scrapy import log
class PushPipeline(object):
    def process_item(self, item, spider):
        print item
        
        # TODO : URLs and image sources may be relative (e.g : '/images/stuff.png')
        log.msg('#' *200)
        log.msg('http://92.39.246.129:9200/object/product/{}'.format(item['_id']))
        log.msg(item.fields)

        data = dict(item.items())
        r = requests.post('http://92.39.246.129:9200/object/product/{}'.format(item['_id']), data=data)
        

        return item
