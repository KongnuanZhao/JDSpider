# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    url = 'http://item.jd.com/1861111.html#product-detail'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    tab_con = soup.find("div", class_='Ptable')
    ptable_items = tab_con.findAll("div", class_='Ptable-item')
    for item in ptable_items:
        h = item.find("h3")
        print h.text
        dts = item.findAll("dt")
        dds = item.findAll("dd")
        for dt, dd in zip(dts, dds):
            print dt.text, ':', dd.text
