# -*- coding: utf-8 -*-
from scrapy.exceptions import IgnoreRequest
from scrapy.http import HtmlResponse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import downloader
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"


# Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36

class CustomMiddlewares(object):
    def process_request(self, request, spider):
        url = str(request.url)
        # dl = downloader.PhantomjsDownloaderMiddleware()
        # content = dl.VisitPersonPage(url)
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
            print '----', e
            return None
        try:
            driver.get(url)
            sleep(5)
            html = driver.page_source.encode('utf-8')
        except Exception as e:
            html = None
            print e
        finally:
            driver.quit()
        # return html
        return HtmlResponse(url, encoding='utf-8', status=200, body=html)

    def process_response(self, request, response, spider):
        if len(response.body) == 100:
            return IgnoreRequest("body length == 100")
        else:
            return response
