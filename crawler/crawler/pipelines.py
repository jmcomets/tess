# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json

from scrapy import log
from scrapy.utils.project import get_project_settings

import debug_settings

class PushPipeline(object):
    _push_to_server = False

    @classmethod
    def push_to_server(cls, value=True):
        cls._push_to_server = value

    def process_item(self, item, spider):
        # TODO : Image URLsmay be relative (e.g : '/images/stuff.png')        
        # log.msg('#' *200)
        # log.msg('http://92.39.246.129:9200/object/product/{}'.format(item['_id']))
        # log.msg(item.fields)

        settings = get_project_settings()
        item.clean()
        
        log.msg('POSTING', self.__class__._push_to_server)
        assert False
        
        if self._push_to_server:
            data = dict(item.items())
            r = requests.post('http://92.39.246.129:9200/object/product/{}'.format(item['_id']), data=json.dumps(data))

        return item