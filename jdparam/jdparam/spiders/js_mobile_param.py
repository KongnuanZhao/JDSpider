import sys

import requests
import scrapy
from bs4 import BeautifulSoup
import json
from jdparam.items import JdparamItem
from jdparam import jdbc

reload(sys)
sys.setdefaultencoding('utf-8')


class JD_Spider(scrapy.Spider):
    start_urls = ['http://www.jd.com/']
    name = 'jd_param'

    def start_requests(self):
        model_result = jdbc.select(jdbc.selectSubModel)
        for model in model_result:
            sub_model_id = model[0]
            url = model[4]
            param_url = url + ''  # product-detail'
            yield scrapy.Request(param_url, meta={'sub_model_id': sub_model_id}, callback=self.parse)

    def parse(self, response):
        sub_mobile_id = response.meta["sub_model_id"]

        item = JdparamItem()
        item['sub_mobile_id'] = sub_mobile_id

        # # store = response.xpath(u'//h3[text()="\u5b58\u50a8"]/text()').extract()
        # store = response.xpath(u'//h3[text()="\u4e3b\u4f53"]/parent::node()//text()').extract()
        # body = response.xpath(u'//h3[text()="\u4e3b\u4f53"]/parent::node()//preceding-sibling::node()//text()').extract()
        # body_dic = {}
        # if len(body) != 0 and len(body % 2 != 0):
        #     for i in range(1, len(body)):
        #         if i % 2 == 0:
        #             body_dic[body[i - 1]] = body[i]
        #     bodyinfos = json.dumps(body_dic, ensure_ascii=False).encode('utf8')
        #     item['bodyinfos'] = bodyinfos

        soup = BeautifulSoup(response.text, 'lxml')
        tab_con = soup.find("div", class_='Ptable')
        ptable_items = tab_con.findAll("div", class_='Ptable-item')
        for item in ptable_items:
            h = item.find("h3")
            if h.text.strip() == '主体':
                dts = item.findAll("dt")
                dds = item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    print dt.text, ':', dd.text




        yield item
