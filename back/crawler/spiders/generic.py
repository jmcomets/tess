from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from items import ProductItem

from collections import defaultdict

import requests
import hashlib
import json

def generate_spider(domain, category, settings):

    # Getting the crawling parameters for the spider
    server_ip = settings['SERVER']
    params_r = requests.get("http://{}/crawl/wrapper/_search?q=name={}".format(server_ip, category))
    params_r.raise_for_status()
    params = json.loads(params_r.text)['hits']['hits'][0]['_source']

    # TODO : debug
    # with open('../../data/wrappers/ldlc.json') as p_f:
    #     params = json.loads(p_f.read())
    
    # Generating a spider class to scrap items from that kind of website    
    class Spider(CrawlSpider):

        name = params['name']
        main_domain = domain
        allowed_domains = [domain]
        start_urls = ['http://{}'.format(domain)]
        fields_xpath = params['rules']
        rules = [Rule(SgmlLinkExtractor(allow=params['pattern']), 'parse_product', follow=True),
                Rule(SgmlLinkExtractor(allow=('.*', )), follow=True)]

        def __init__(self, *args, **kwargs):
            super(Spider, self).__init__(*args, **kwargs)
            # TODO : See if we can avoid creating a class per spider type  

        def parse_product(self, response):
            x = HtmlXPathSelector(response)

            product = ProductItem()

            product['url'] = response.url
            product['_id'] = hashlib.sha256(response.url).hexdigest()

            for field in product.fields:
                if field in {'url', '_id'}:
                    continue
                xpath = self.fields_xpath[field]
                product[field] = x.select(xpath).extract()

            return product

    return Spider