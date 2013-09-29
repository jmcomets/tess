#!/usr/bin/env python
# -*- coding: utf-8 -*-


# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy import log
import urlparse

PRICE_MAP = {('€', 'EUR', 'EURO') : 'EUR',
             ('£', 'GBP', 'POUND') : 'GBP',
             ('$', 'USD', 'DOLLAR') : 'USD'}

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
            if thumbnail.startswith('/') and not thumbnail.startswith('//'):
                self['thumbnail'][i] = 'http://' + domain + self['thumbnail'][i]

        # TODO: Parsing prices
        if not self['price']:
            return
        
        raw_price = self['price'][0].encode('utf-8').replace(' ', '').strip()
        self['price'] = dict()
        self['price']['raw'] = raw_price
        price = raw_price

        # Detecting currency and removing it
        price_cur = None
        for signatures, currency in PRICE_MAP.iteritems():
            if any(signature in price for signature in signatures):
                price_cur = currency
                for signature in signatures:
                    price.replace(signature, '')
                break

        if 1 <= len(price.split(',')) <= 2:
            price = price.replace(',', '.')
            self['price']['value'] = float(price)

        # DEBUG ONLY:
        if price_cur is None:
            price_cur = 'EUR'

        self['price']['currency'] = price_cur
