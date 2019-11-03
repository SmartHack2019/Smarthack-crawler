import scrapy
import csv

global_dict = {}

class QuotesSpider(scrapy.Spider):
    name = "num_of_pages"

    def start_requests(self):

        base_url = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/news-analysis.html?fourWayKey='
        with open('companies.csv') as f:
            reader = csv.reader(f)
            companies = list(reader)
        
        urls = []
        for c in companies:
            global_dict[c[2]] = c[0]
            urls.append(base_url + c[2])

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
      
        num_of_pages = response.css('p.floatsx::text').get()
        page_number = num_of_pages[10:].replace(' ', '').replace('\n', '')

        with open('pages.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([global_dict[response.url[-21:]] ,response.url, page_number])
        