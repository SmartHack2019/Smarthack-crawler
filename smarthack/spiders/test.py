import scrapy
import re
import csv
import sys
import requests

company_code_dict = {}


class QuotesSpider(scrapy.Spider):
    name = "test"

    def start_requests(self):
        u1 = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/news-analysis.html?fourWayKey='
        u2 = '&page='

        with open("pages.csv") as f:
            reader = csv.reader(f)
            companies = list(reader)
        


        
        
        # company_ids = [c[0] for c in companies]
        

        first_urls = []
        url_dict = {}
        for c in companies:
            company_code_dict[c[1]] = c[0]
            first_urls.append(c[1])
            url_dict[c[1]] = c[2]
            
        
        urls = []
        for u in first_urls:
            for i in range (1, int(url_dict[u])):
                urls.append(u + u2 + str(i))
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        to_measure = 'https://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/news-analysis.html?fourWayKey='



        link = response.url[:139]

        company_code = company_code_dict[link]

        
        base_url = 'https://www.londonstockexchange.com'
        like = '/exchange/news/market-news/market-news-detail/'
        text = response.body


        auxxx = [m.start() for m in re.finditer(like, text)]
        
        # print link
        links_to_add = []
        for aux in auxxx:
            link_to_add = base_url + like + company_code +'/'+ text[aux+len(like) + len(company_code) + 1: aux + len(like) + len(company_code) + 1 + 13]
            links_to_add.append(link_to_add)

        # print links_to_add
        titles = [title.replace('\t', '').replace('\n', '') for title in response.css('td.text-left a::text').getall()]

        
        # # with open(filename, 'w') as f:
        # #     for aux in auxxx:
        # #         f.write(base_url + text[aux: aux+len(like)+13])
        # #         f.write('\n')
        # toWriteList = [(base_url + text[aux: aux + len(like) + 13]) for aux in auxxx]
        with open('links.csv', 'a') as f:
            wrt = csv.writer(f)
            auxax = []
            for i in range(len(titles)):
                auxax = [company_code, titles[i].encode('utf-8'), links_to_add[i]]
                wrt.writerow(auxax)                
        