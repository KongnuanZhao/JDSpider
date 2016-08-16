# -*-coding:utf-8-*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
import jdbc

UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

next_links = []


def getUrl(url):
    sleep(1)
    if url is None:
        return
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError, e:
        print e
        for i in range(3):
            response = requests.get(url)
            if response is not None:
                break
    soup = BeautifulSoup(response.text, 'lxml')
    next_link = soup.find('a', class_='pn-next')
    if next_link is not None:
        print next_link['href']
        next_links.append('http://list.jd.com' + next_link['href'])
        getUrl('http://list.jd.com' + next_link['href'])
    else:
        getUrl(next_link)
        # return response


def getPage(url):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        UA
    )
    #     dcap["phantomjs.page.customHeaders.Referer"] = (
    #         url
    #     )
    dcap["takesScreenshot"] = (False)
    # t0 = time.time()
    try:
        driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--load-images=no'])
        driver.set_page_load_timeout(240)
        driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')

        driver.execute('executePhantomScript', {'script': '''
                    var page = this;
                    page.onResourceRequested = function(requestData, request) {
                        if ((/http:\/\/.+?\.css/gi).test(requestData['url']) || requestData['Content-Type'] == 'text/css') {
                            request.abort();
                        }
                    }
                    ''', 'args': []})
    except Exception, e:
        print e
        return None
    try:
        driver.get(url)
        sleep(3)
        html = driver.page_source
        # print html
    except Exception as e:
        html = None
        print e
    finally:
        driver.quit()
    return html


if __name__ == '__main__':
    brands = jdbc.select(jdbc.selectBrand)
    for brand in brands:
        next_links = []
        brand_id = brand[0]
        brand_name = brand[1]
        url = brand[4]
        next_links.append(url)
        print 'current brand', brand_id
        getUrl(url)
        for cur_link in next_links:
            print 'current fetch...', cur_link
            value_list = []
            html = getPage(cur_link)
            soup = BeautifulSoup(html, 'lxml')
            mobiles = soup.findAll('div', class_='gl-i-wrap j-sku-item')
            for mobile in mobiles:
                price = mobile.find('strong', class_='J_price')
                name_div = mobile.find('div', class_='p-name')
                name = name_div.find('em')
                url = name_div.find('a')['href'].strip()
                print brand_id, name.text.strip(), url, price.text.strip()
                value_list.append((brand_id, name.text.strip(), url, price.text.strip()))
            jdbc.insert(value_list, jdbc.insertModel)



            # url = 'http://list.jd.com/list.html?cat=9987,653,655&ev=exbrand%5F8557&go=0'
            # getUrl(url)
            # print requests.get(url).text
