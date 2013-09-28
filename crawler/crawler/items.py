#!/usr/bin/env python
# -*- coding: utf-8 -*-


# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
import urlparse

PRICE_MAP = {['€', 'EUR', 'EURO'] : 'EUR',
             ['£', 'GBP', 'POUND'] : 'GBP',
             ['$', 'USD', 'DOLLAR']: 'USD'}

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
        raw_price = self['price'].strip()
        self['price'] = None

        for signatures, currency in PRICE_MAP.iteritems():
            for signature in signatures:
                if signature in raw_price.startswith(signature) or raw_price.endswith('raw_price'):
                    clean_price = raw_price.replace(signature, '')
                    self['price'] = {'raw': raw_price,
                                     'value': float(clean_price),
                                     'currency': currency}
                    break
            
            if self['price']:
                break

        if self['price'] is None:
            self['price'] = {'raw': raw_price, 'value' : None, 'currency': None}
