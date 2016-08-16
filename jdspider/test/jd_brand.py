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


def getUrl(url):
    s = requests.session()
    headers = {"User-Agent": UA, "Connection": "keep-alive",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "Accept-Language": "zh-cn,en-us;q=0.7,en;q=0.3", "Host": "www.stats.gov.cn",
               "Accept-Encoding": "gzip, deflate"}
    s.headers.update(headers)
    try:
        response = s.get(url)
    except requests.exceptions.ConnectionError, e:
        print e
        for i in range(3):
            response = s.get(url)
            if response is not None:
                return response
    return response


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
        sleep(5)
        driver.find_element_by_xpath("//*[@id='J_selector']/div[2]/div/div[3]/a[1]").click()
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
    url = 'http://list.jd.com/list.html?cat=9987%2C653%2C655&go=0'
    html = getPage(url)
    soup = BeautifulSoup(html, 'lxml')
    brands = soup.find('div', class_='J_selectorLine s-brand')
    ul = brands.find('ul', class_='J_valueList v-fixed', id='brandsArea')
    a_list = ul.findAll('a')
    value_list = []
    for a in a_list:
        print a['title'], a['href']
        link = 'http://list.jd.com' + a['href']
        value_list.append((a['title'], a['href'], link))
    jdbc.insert(value_list, jdbc.insertBrand)


