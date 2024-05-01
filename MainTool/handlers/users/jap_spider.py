import os
from multiprocessing import Process 
import json
import scrapy
import re
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

# Create Process around the CrawlerRunner
class CrawlerRunnerProcess(Process):
    def __init__(self, spider):
        Process.__init__(self)
        self.runner = CrawlerRunner(settings={
        "FEEDS": {
            "/home/projects/MainTool/services.json": {"format": "json"},
        }})
        self.spider = spider

    def run(self):
        deferred = self.runner.crawl(self.spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)


# The wrapper to make it run multiple spiders, multiple times
def run_spider(spider):
    crawler = CrawlerRunnerProcess(spider)
    crawler.start()
    crawler.join()

ids = ['6685', '7110', '6583', '1365']

class MainToolSpider(scrapy.spiders.Spider):
    name = 'maintool_spider'
    allowed_domains = ['justanotherpanel.com']
    start_urls = ['https://justanotherpanel.com/services']

    def parse(self, response):
        list_of_services = response.css('tbody>tr.service')

        for service in list_of_services:
            # yield {'td': service} 

            tds = service.css('td::text').getall()
            id = tds[0].replace('\n', '').strip()
            if id in ids:
                avg_time_raw = tds[-1].split('data-average')[-1].split()
                hs_mins = []
                avg_time = 10000000
                for elem in avg_time_raw:
                    try:
                        hs_mins.append(int(elem))
                    except ValueError:
                        pass
                if len(hs_mins) == 2:
                    avg_time = hs_mins[0]*60 + hs_mins[1]
                elif len(hs_mins) == 1:
                    avg_time = hs_mins[0]
            
                yield {'id': id, 'avg_time': avg_time}    



def services_getter():
    run_spider(MainToolSpider)

    services = []

    with open('/home/projects/MainTool/services.json') as f:
        d = json.load(f)
        for service in d:
            services.append((service['id'], service['avg_time']))


    os.remove('/home/projects/MainTool/services.json')

    return dict(services)


