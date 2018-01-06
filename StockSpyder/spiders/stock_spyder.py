import scrapy


class StockSpider(scrapy.Spider):
    name = "stock"



    def start_requests(self):
        urls = [
            "https://www.finanzen.net/timesandsales/ISRA_VISION@stBoerse_xetra@inEnd_",
            "https://www.finanzen.net/timesandsales/Bayer@stBoerse_xetra@inEnd_",
            "https://www.finanzen.net/timesandsales/Adidas@stBoerse_xetra@inEnd_",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        stockname = page.split("@")[0]
        filename = 'TimesAndSales-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        # data = response.xpath('//table/tr[count(td)=4]').extract()
        timeofSale = response.xpath('//table/tr[count(td)=4]/td[1]/text()').extract()
        price = response.xpath('//table/tr[count(td)=4]/td[2]/text()').extract()
        numstocks = response.xpath('//table/tr[count(td)=4]/td[3]/text()').extract()

        for item in zip(timeofSale, price, numstocks):
            scraped_info = {
                'Stock': stockname,
                'timeofSale': item[0],
                'price': item[1],
                'numstocks': item[2]
            }
            yield scraped_info

        # follow next page links
        next_page = response.xpath('.//a[@class="btn-more pull-sm-right"]/@href').extract()
        if next_page:
            next_href = next_page[0]
            next_page_url = response.urljoin(next_href)
            print('Next page url: ', next_page_url)
            request = scrapy.Request(url=next_page_url, callback=self.parse)
            yield request