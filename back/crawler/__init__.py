from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from spiders.generic import generate_spider
from scrapy.utils.project import get_project_settings

import sys
import pickle
from learning import predict

def setup_crawler(domain, category, settings, spider_cache={}):
    # TODO : detect the category

    if category in spider_cache:
        SpiderClass = spider_cache[category]
    else:
        SpiderClass = generate_spider(domain=domain, category=category, settings=settings)
    
    spider = SpiderClass()

    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)

    crawler.start()


if __name__ == '__main__':
    
    # Setting the 'push' parameter (pushing scrapped objects to server, or not)
    settings = get_project_settings()
    settings.overrides['push'] = '--prod' in sys.argv

    # Fetching crawled domains
    domains = list()
    for arg in sys.argv:
        if ':' in arg:
            domains.append(arg.split(':'))
    # Fallback: default domains
    if not domains:
        domains = {('ldlc.com', 'ldlc')}

    # Setting up a crawler per domain
    spider_cache = dict()
    for domain, category in domains:
        setup_crawler(domain, category, settings, spider_cache)


    # Setting up the predictor
    with open(settings['PREDICTOR_PATH']) as predictor_file:
        # settings.PREDICTOR = predict.Predictor.from_file(predictor_file)
        pass

    # Setting up the logger
    loglevel = log.DEBUG if '--debug' in sys.argv else log.INFO
    log.start(loglevel=loglevel, logstdout=True)

    # Running the crawlers
    reactor.run()