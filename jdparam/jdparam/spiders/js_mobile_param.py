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
            param_url = url + '#product-detail'
            yield scrapy.Request(param_url, meta={'sub_model_id': sub_model_id}, callback=self.parse)

    def parse(self, response):
        sub_mobile_id = response.meta["sub_model_id"]

        item = JdparamItem()
        item['sub_mobile_id'] = sub_mobile_id
        item['bodyinfos'] = ""
        item['base_info'] = ""
        item['mobile_os'] = ""
        item['mobile_cpu'] = ""
        item['mobile_internet'] = ""
        item['mobile_store'] = ""
        item['mobile_screen'] = ""
        item['front_camera'] = ""
        item['rear_camera'] = ""
        item['battery_info'] = ""
        item['data_interface'] = ""
        item['mobile_feature'] = ""
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
        for p_item in ptable_items:
            h = p_item.find("h3")
            # print h.text.encode()
            if h.text.strip() == u'\u4e3b\u4f53':
                body_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    body_dic[key] = value
                bodyinfos = json.dumps(body_dic, ensure_ascii=False).encode('utf8')
                item['bodyinfos'] = bodyinfos
            if h.text.strip() == u'\u57fa\u672c\u4fe1\u606f':
                baseinfo_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    baseinfo_dic[key] = value
                baseinfo = json.dumps(baseinfo_dic, ensure_ascii=False).encode('utf8')
                item['base_info'] = baseinfo
            if h.text.strip() == u'\u64cd\u4f5c\u7cfb\u7edf':
                mobile_os_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_os_dic[key] = value
                mobile_os = json.dumps(mobile_os_dic, ensure_ascii=False).encode('utf8')
                item['mobile_os'] = mobile_os
            if h.text.strip() == u'\u4e3b\u82af\u7247':
                mobile_cpu_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_cpu_dic[key] = value
                mobile_cpu = json.dumps(mobile_cpu_dic, ensure_ascii=False).encode('utf8')
                # print mobile_cpu
                item['mobile_cpu'] = mobile_cpu
            if h.text.strip() == u'\u7f51\u7edc\u652f\u6301':
                mobile_internet_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_internet_dic[key] = value
                mobile_internet = json.dumps(mobile_internet_dic, ensure_ascii=False).encode('utf8')
                item['mobile_internet'] = mobile_internet
            if h.text.strip() == u'\u5b58\u50a8':
                mobile_store_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_store_dic[key] = value
                mobile_store = json.dumps(mobile_store_dic, ensure_ascii=False).encode('utf8')
                item['mobile_store'] = mobile_store
            if h.text.strip() == u'\u5c4f\u5e55':
                mobile_screen_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_screen_dic[key] = value
                mobile_screen = json.dumps(mobile_screen_dic, ensure_ascii=False).encode('utf8')
                item['mobile_screen'] = mobile_screen
            if h.text.strip() == u'\u524d\u7f6e\u6444\u50cf\u5934':
                front_camera_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    front_camera_dic[key] = value
                front_camera = json.dumps(front_camera_dic, ensure_ascii=False).encode('utf8')
                item['front_camera'] = front_camera
            if h.text.strip() == u'\u540e\u7f6e\u6444\u50cf\u5934':
                rear_camera_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    rear_camera_dic[key] = value
                rear_camera = json.dumps(rear_camera_dic, ensure_ascii=False).encode('utf8')
                item['rear_camera'] = rear_camera
            if h.text.strip() == u'\u7535\u6c60\u4fe1\u606f':
                battery_info_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    battery_info_dic[key] = value
                battery_info = json.dumps(battery_info_dic, ensure_ascii=False).encode('utf8')
                item['battery_info'] = battery_info
            if h.text.strip() == u'\u6570\u636e\u63a5\u53e3':
                data_interface_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    data_interface_dic[key] = value
                data_interface = json.dumps(data_interface_dic, ensure_ascii=False).encode('utf8')
                item['data_interface'] = data_interface
            if h.text.strip() == u'\u624b\u673a\u7279\u6027':
                mobile_feature_dic = {}
                dts = p_item.findAll("dt")
                dds = p_item.findAll("dd")
                for dt, dd in zip(dts, dds):
                    key = dt.text.strip()
                    value = dd.text.strip()
                    # print key, ':', value
                    mobile_feature_dic[key] = value
                mobile_feature = json.dumps(mobile_feature_dic, ensure_ascii=False).encode('utf8')
                item['mobile_feature'] = mobile_feature
        # print item
        yield item
