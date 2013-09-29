# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json

from scrapy import log
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

class PushPipeline(object):

    def process_item(self, item, spider):
        # TODO : Image URLsmay be relative (e.g : '/images/stuff.png')        
        # log.msg('#' *200)
        # log.msg('http://92.39.246.129:9200/object/product/{}'.format(item['_id']))
        # log.msg(item.fields)

        settings = get_project_settings()
        item.clean()

        if not item['name']: # or not item['price']:
            raise DropItem

        if spider.settings.overrides['push']:
            data = dict(item.items())
            r = requests.post('http://{}/object/product/{}'.format(spider.settings['SERVER'], item['_id']), data=json.dumps(data))

        return item