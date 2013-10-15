from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log

from items import ProductItem, PersonItem
#from learning import predict

from collections import defaultdict, Counter

import requests
import hashlib
import json
import lxml.html

ITEM_MAP = {'product' : ProductItem, 'person': PersonItem}

def generate_spider(domain, category, settings):

    # Getting the crawling parameters for the spider
    server_ip = settings['SERVER']
    params_r = requests.get("http://{}/crawl/wrapper/_search?q=_id={}".format(server_ip, category))
    params_r.raise_for_status()
    params = json.loads(params_r.text)['hits']['hits'][0]['_source']

    log.msg('"{}" using parameters -> {}'.format(domain, params))

    # TODO : debug
    # with open('../../data/wrappers/ldlc.json') as p_f:
    #     params = json.loads(p_f.read())

    # Generating a spider class to scrap items from that kind of website
    class Spider(CrawlSpider):

        name = params['name']
        main_domain = domain
        allowed_domains = [domain]
        start_urls = ['http://{}'.format(domain)]
        if 'start_urls' in params:
            start_urls += params['start_urls']

        fields_xpath = params['rules']
        rules = [Rule(SgmlLinkExtractor(allow=params['pattern']), 'parse_product', follow=True),
                 Rule(SgmlLinkExtractor(allow=('.*', )), 'detect_product',follow=True)]

        category = params['category'] if 'category' in params else 'product'
        item_type = ITEM_MAP[category]

        def detect_product(self, response):
            """ Detects if the crawled page is a product page """

            classes_freq = Counter(lxml.html.fromstring(response.body).xpath('//@class'))
            # prediction = predict.make_prediction(classes_freq.items())

            # log.msg('###########\n\n {} -> {} \n\n###############'.format(response.url, prediction))

        def parse_product(self, response):
            """ Parses a product page """

            x = HtmlXPathSelector(response)

            product = self.item_type()

            product['url'] = response.url

            for field in product.fields:
                if field in {'url', '_id'}:
                    continue
                xpath = self.fields_xpath[field]
                product[field] = x.select(xpath).extract()

                # Removing trailing spaces from extracted data
                for i, element in enumerate(product[field]):
                    product[field][i] = element.strip()

                # log.msg('Applying "{}" for "{}" -> {}'.format(xpath, field, product[field]))

            #product['_id'] = hashlib.sha256(response.url).hexdigest()
            product['_id'] = hashlib.sha256('{}{}'.format(product['name'], product['description'])).hexdigest()


            return product

    return Spider
