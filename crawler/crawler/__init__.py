
if __name__ == '__main__':
    from twisted.internet import reactor
    from scrapy.crawler import Crawler
    from scrapy.settings import Settings
    from scrapy import log
    from spiders.ldlc import GenericSpider
    from scrapy.utils.project import get_project_settings

    def setup_crawler(domain):
        # TODO : detect the category
        spider = GenericSpider(domain=domain, category='ldlc')

        crawler = Crawler(get_project_settings())
        crawler.configure()
        crawler.crawl(spider)

        crawler.start()
        
        print '"{}" crawler started'.format(domain)

    for domain in ['ldlc.com']:
        setup_crawler(domain)

    log.start(loglevel=log.DEBUG)
    reactor.run()