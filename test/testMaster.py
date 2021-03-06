#!/usr/bin/env python
#coding:utf-8

from dpspider.masterspider import MasterSpider

class MyMasterSpider(MasterSpider):
    def __init__(self):
        MasterSpider.__init__(self)
        self.listUrls = ['http://www.tmtpost.com/new/%d'%page for page in range(1,11)]
        self.serverHost = '127.0.0.1'
        self.serverAuthkey = b'test'
        self.mysqlHost = ''
        self.mysqlUser = ''
        self.mysqlPassword = ''
        self.mysqlDb = ''
        self.mysqlTableName = ''
        # self.isInsertMysql = True
        # self.isUseRedis = True
        # self.proxyEnable = True
        #self.isDebug = 'print'

    def parseList(self,data,response):
        urls = []
        if data:
            loops = data.xpathAll('//h3/a/@href')
            for item in loops:
                url = 'http://www.tmtpost.com%s'%item.str()
                urls.append(url)
        return urls

    def parsePage(self,data,response):
        jsonData = {}
        if data:
            TITLE = data.xpathOne('//h1').bytes().strip()
            URL = response.request.url
            CTIME = data.xpathOne('//span[contains(@class,"time")]').bytes().strip()
            SUMMERY = data.xpathOne('//p[@class="post-abstract"]/text()[2]').bytes().strip()
            jsonData = {
                'TITLE': TITLE,
                'URL': URL,
                'CTIME': CTIME,
                'SUMMERY': SUMMERY,
                self.redisMd5Key: self.md5(URL)
            }
        return jsonData

if __name__ == '__main__':
    dp = MyMasterSpider()
    dp.run()
