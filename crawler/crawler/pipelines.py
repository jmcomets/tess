# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import json

from scrapy import log

class PushPipeline(object):
    def process_item(self, item, spider):
        print item
        
        # TODO : Image URLsmay be relative (e.g : '/images/stuff.png')        
        # log.msg('#' *200)
        # log.msg('http://92.39.246.129:9200/object/product/{}'.format(item['_id']))
        # log.msg(item.fields)

        data = dict(item.items())

        if 'thumbnail' in data:
            thumbnails = data['thumbnail']
            for i, thumbnail in enumerate(thumbnails):
                if thumbnail.startswith('/'):
                    thumbnails[i] = 'http://' + spider.main_domain + thumbnails[i]

        r = requests.post('http://92.39.246.129:9200/object/product/{}'.format(item['_id']), data=json.dumps(data))

        return item