from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from items import ProductItem

from collections import defaultdict
import requests
import hashlib
import json

FIELDS = {'url', '_id', 'title', 'description', 'thumbnail', 'price'}

class GenericSpider(CrawlSpider):
    name = 'ldlc'
    allowed_domains = ['ldlc.com']
    start_urls = ['http://www.ldlc.com/informatique/piece/disque-dur-ssd/cint4297/']
    rules = [Rule(SgmlLinkExtractor(allow=['/fiche/PB\d+\.html']), 'parse_product', follow=True)]

    def __init__(self, domain, category, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)

        # domain=None, start_urls=[], fields_xpath=defaultdict(str), allowed_patterns=[]

        # params_r = requests.get('http://92.39.246.129/crawl/wrapper/{}'.format(category))
        # params_r.raise_for_status()

        with open('../../data/wrappers/ldlc.json') as wrapper_file:
            params = json.loads(wrapper_file.read())
            start_urls = ['http://www.ldlc.com/informatique/piece/disque-dur-ssd/cint4297/'] # ['http://{}'.format(domain)]
            fields_xpath = params['rules']
            allowed_patterns = params['pattern']

        self.allowed_domains = [domain]
        self.start_urls = start_urls
        self.fields_xpath = fields_xpath
        self.rules = [Rule(SgmlLinkExtractor(allow=allowed_patterns), 'parse_product', follow=True)]


    def parse_product(self, response):
        x = HtmlXPathSelector(response)

        product = ProductItem()

        product['url'] = response.url
        product['_id'] = hashlib.sha256(response.url).digest()

        for field in product.fields:
            if field in {'url', '_id'}:
                continue
            xpath = self.fields_xpath[field]
            product[field] = x.select(xpath).extract()


        # TODO : URLs and image sources may be relative (e.g : '/images/stuff.png')

        # product['title'] = x.select("//span[@class='fn designation_courte'][1]/text()").extract()
        # product['description'] = x.select("//span[@id='ctl00_cphMainContent_lbChapeau'][1]/text()").extract()
        # product['thumbnail'] = x.select("//img[@id='ctl00_cphMainContent_ImgProduct'][1]/@src").extract()
        # product['price'] = x.select("//span[@class='price sale']/text()").extract()

        #requests.post('http://92.39.246.129/object/product/{}'.format(product['_id']), params=product.__dict__)
        
        return product