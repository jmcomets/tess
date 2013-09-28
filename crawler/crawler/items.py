#!/usr/bin/env python
# -*- coding: utf-8 -*-


# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import urlparse
#PRICE_MAP = {'€' : 'EUR', '£' : }

class ProductItem(Item):
    _id = Field()
    url = Field()
    name = Field()
    description = Field()
    brand = Field()
    model = Field()
    price = Field()
    thumbnail = Field()

    def clean(self):
        domain = urlparse.urlparse(self['url']).netloc 

        # Correcting absolute image URLs
        for i, thumbnail in enumerate(self['thumbnail']):
            if thumbnail.startswith('/'):
                self['thumbnail'][i] = 'http://' + domain + self['thumbnail'][i]

        # TODO: Parsing prices