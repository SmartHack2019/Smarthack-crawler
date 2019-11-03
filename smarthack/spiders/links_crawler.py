import scrapy
import re
import csv

class QuotesSpider(scrapy.Spider):
    name = "links_crawler"

    def start_requests(self):

        base_url = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/indices/summary/summary-indices-constituents.html?index=UKX&page='
        urls = [base_url + str(i) for i in range(1, 7)]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        like = '/exchange/prices-and-markets/stocks/summary/company-summary/'
        text = response.body

        companies_links = [m.start() for m in re.finditer(like, text)]
        links = [text[curr: curr+len(like)+26] for curr in companies_links]

        company_names = response.css('td.name a::text').getall()
        company_codes = response.css('tr td[scope=row]::text').getall()
        links = [link[-26:-5] for link in links]        
        with open("companies.csv", "a") as f:
            writer = csv.writer(f)
            toAdd = []
            for i in range(len(links)):
                toAdd.append([company_codes[i], company_names[i], links[i]])
            writer.writerows(toAdd)
        # prices = response.css('tr td::text').getall()
        # print prices
        # print company_names
        # print links

        # company_name = response.css("td.name ")
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wt') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)