import sys

import requests
import scrapy
from bs4 import BeautifulSoup

from jdspider.items import JdSubModelItem
from jdspider.test import jdbc

reload(sys)
sys.setdefaultencoding('utf-8')


class JD_Spider(scrapy.Spider):
    start_urls = ['http://www.jd.com/']
    name = 'jd_spider'

    def start_requests(self):
        model_result = jdbc.select(jdbc.selectModel)
        for model in model_result:
            model_id = model[0]
            brand_id = model[1]
            url = model[3]
            if url.find('http') != -1:
                pass
            else:
                url = 'http:' + url
            jd_respone = requests.get(url)
            soup = BeautifulSoup(jd_respone.text, 'lxml')
            choose = soup.find('div', class_='summary p-choose-wrap')
            if choose is None:
                choose = soup.find('div', id='choose')
            items = choose.findAll('div', class_='item')
            for item in items:
                href = item.find('a')['href']
                href = 'http:' + href
                yield scrapy.Request(href, meta={'brand_id': brand_id, 'model_id': model_id}, callback=self.parse)

    def parse(self, response):
        brand_id = response.meta["brand_id"]
        model_id = response.meta["model_id"]
        item = JdSubModelItem()
        name = response.xpath("//div[@class='p-info lh']/div[@class='p-name']/text()").extract()
        price = response.xpath("//div[@class='p-info lh']/div[@class='p-price']/strong/text()").extract()
        if len(name) != 0 and len(price) != 0:
            item['brand_id'] = brand_id
            item['model_id'] = model_id
            item['name'] = name[0]
            item['price'] = price[0]
            item['url'] = response.url
            print brand_id, model_id, name[0], price[0], response.url
        else:
            print '----', price, '+++++', name
        yield item
