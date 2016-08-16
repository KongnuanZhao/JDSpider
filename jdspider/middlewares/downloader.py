# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class PhantomjsDownloaderMiddleware(object):
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["takesScreenshot"] = (False)
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

    def VisitPersonPage(self, url):
        print('正在加载网站.....')
        self.driver.get(url)
        time.sleep(3)
        content = self.driver.page_source
        print('网页加载完毕.....')
        return content

    def __del__(self):
        self.driver.quit()
