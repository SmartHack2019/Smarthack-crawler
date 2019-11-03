import scrapy
import csv

global_dict = {}


class QuotesSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        # base_url = 'https://www.londonstockexchange.com'

        with open('links.csv', 'r') as f:
            reader = csv.reader(f)
            lines = list(reader)
        
        urls = []
        for line in lines:
            urls.append(line[2])
           
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        link = response.url

        content1 = ' '.join(response.css('span::text').getall())
        content2 = ' '.join(response.css('p::text').getall())
        
         
        content = content1 + ' ' + content2
        toAdd = [link, content.encode('utf-8')]
        # print toAdd
        with open("data.csv", 'a') as f:
            reader = csv.writer(f)
            reader.writerow(toAdd)

      