from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from spiders.generic import generate_spider
from scrapy.utils.project import get_project_settings

def setup_crawler(domain, spider_cache={}):
    # TODO : detect the category
    category = 'ldlc'

    if category in spider_cache:
        SpiderClass = spider_cache[category]
    else:
        SpiderClass = generate_spider(domain=domain, category=category)
    
    spider = SpiderClass()

    crawler = Crawler(get_project_settings())
    crawler.configure()
    crawler.crawl(spider)

    crawler.start()


if __name__ == '__main__':
    
    spider_cache = dict()
    for domain in ['ldlc.com']:
        setup_crawler(domain, spider_cache)

    log.start(loglevel=log.INFO, logstdout=True)
    reactor.run()