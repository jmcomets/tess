from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from crawler.items import ProductItem

class LdlcSpider(CrawlSpider):
    name = 'ldlc'
    allowed_domains = ['ldlc.com']
    start_urls = ['http://www.ldlc.com/informatique/piece/disque-dur-ssd/cint4297/']


    rules = [Rule(SgmlLinkExtractor(allow=['/fiche/PB\d+ \.html']), 'parse_product', follow=True)]

    def parse_product(self, response):
        x = HtmlXPathSelector(response)

        product = ProductItem()
        product['url'] = response.url
        product['name'] = x.select("//span[@class='fn designation_courte'][0]/text()").extract()
        product['description'] = x.select("//span[@id='ctl00_cphMainContent_lbChapeau'][0]/text()").extract()
        product['price'] = x.select("//span[@class='price sale'][0]/text()").extract()
        return product