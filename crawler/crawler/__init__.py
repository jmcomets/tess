from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
from spiders.generic import generate_spider
from scrapy.utils.project import get_project_settings
from pipelines import PushPipeline

import sys

def setup_crawler(domain, category, spider_cache={}):
    # TODO : detect the category

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
    
    settings = get_project_settings()
    if '--prod' in sys.argv:
        PushPipeline.push_to_server()
    domains = list()
    for arg in sys.argv:
        if ':' in arg:
            domains.append(arg.split(':'))
    
    if not domains:
        domains = {('ldlc.com', 'ldlc')}

    spider_cache = dict()
    for domain, category in domains:
        setup_crawler(domain, category, spider_cache)

    log.start(loglevel=log.DEBUG, logstdout=True)
    reactor.run()