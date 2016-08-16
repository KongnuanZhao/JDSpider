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
    url = 'http://item.jd.com/1861111.html'
    html = getPage(url)
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('div', class_='sku-name').text.strip()
    print name
    price = soup.find('span', class_='p-price').text
    print price
