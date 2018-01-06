import scrapy
import pandas as pd

from scrapy.crawler import CrawlerProcess
from spiders.stock_spyder import StockSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

import json
from pprint import pprint


json1_file = open('D:\SourceExt\Spyders\Data\items.json')
json1_str = json1_file.read()
json1_data = json.loads(json1_str)


StockID = []
timeOfSales = []
volumes = []
prices = []

for item in json1_data:
    prices.append(item['price'])
    timeOfSales.append(item['timeofSale'])
    volumes.append(item['numstocks'])
    StockID.append(item['Stock'])
    df = pd.DataFrame(data=item)

print(prices)
print(volumes)


#json1_data1 = json.dumps(json1_data, sort_keys=True, indent=4)
#print (json.dumps(json1_data, sort_keys=True, indent=4))
#pprint(json1_data)



configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()
runner.crawl(StockSpider)
runner.crawl(StockSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())


reactor.run() # the script will block here until the crawling is finished