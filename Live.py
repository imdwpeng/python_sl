'''
@Author: Eric
@Date: 2020-07-14 20:39:33
LastEditors: Dong
LastEditTime: 2020-12-29 22:09:48
'''
import re
import requests
from lxml import etree
from fake_useragent import UserAgent


class Live:
    def get_search_live(self, keyword, date, totalRatio):
        self.name = ''
        self.uid = ''
        self.singleRatio = 0
        self.searchUrl = "https://dy.feigua.cn/home/search"
        self.url = "https://dy.feigua.cn/Blogger/LiveAnalysis?page=1&uid="
        self.ua = UserAgent()
        self.headers = {
            "Cookie": self.cookie,
            "User-Agent": self.ua.random  # 获取随机的User-Agent
        }
        res = requests.get(self.searchUrl + "?keyword=" + keyword + "&period=" + date, headers=self.headers)
        s = etree.HTML(res.text)
        self.name = s.xpath('//*[@id="js-qc-blogger-container"]/div[1]/div/div/div[1]/text()')[0].strip() if s.xpath('//*[@id="js-qc-blogger-container"]/div') else ''
        detailUrl = s.xpath('//*[@id="js-qc-blogger-container"]/div[1]/a')
        if self.name and detailUrl:
            detailUrl = 'https://dy.feigua.cn/BloggerNew' + s.xpath('//*[@id="js-qc-blogger-container"]/div[1]/a/@href')[0][9:]
            self.uid = self.get_uid(detailUrl)
            self.get_all_session(totalRatio)
        else:
            print(keyword + ' 无此播主')

    def get_uid(self, url):
        res = requests.get(url, headers=self.headers)
        s = etree.HTML(res.text)
        uid = s.xpath('//*[@id="btnAddBookTraceLive"]/@data-uid')[0]
        return uid

    # 获取直播场次
    def get_all_session(self, totalRatio):
        res = requests.get(self.url + str(self.uid), headers=self.headers)
        s = etree.HTML(res.text)
        tr = s.xpath('//table/tbody/tr')
        noResult = s.xpath('//*[@id="none_data_tip"]')
        params = []
        nickNames = []
        startTimes = []
        if len(noResult) == 1:
            print(self.name + "无数据")
        elif len(tr):
            for i in range(len(tr)):
                nickName = s.xpath('//table/tbody/tr[{}]/td[1]/div/div[2]/text()'.format(i + 1))[0].strip()
                startTime = s.xpath('//table/tbody/tr[{}]//td[2]/span/text()'.format(i + 1))[0].strip()
                a = s.xpath('//table/tbody/tr[{}]/td[9]/div/a/@href'.format(i + 1))[0]
                params.append(a[13:])
                nickNames.append(nickName)
                startTimes.append(startTime)
        else:
            print("Error！")

        if len(params):
            # 每场直播的进度占比
            sessionRatio = totalRatio / float(len(params))
            for i in range(len(params)):
                print('================' + self.name + str(i + 1) + '==================')
                page = 1
                self.get_all_products(params[i], nickNames[i], startTimes[i], 1, sessionRatio)

    # 获取每场直播的产品
    def get_all_products(self, param, nickName, startTime, page, sessionRatio):
        hasData = self.get_detail(param, nickName, startTime, page, sessionRatio)
        if hasData:
            page += 1
            self.get_all_products(param, nickName, startTime, page, sessionRatio)

    # 获取每个产品的详情
    def get_detail(self, param, nickName, startTime, page, sessionRatio):
        print(page)
        res = requests.get(
            'https://dy.feigua.cn/LiveDetail/ProductList?uid=' + self.uid + '&' + param + '&shopId=&cateid=&conversionFlag=0&partial=1&keyword=&sort=0&page=' + str(
                page) + '&_=1608820281487', headers=self.headers)
        s = etree.HTML(res.text)
        prev = '//table/tbody/' if page == 1 else '//'
        tr = s.xpath(prev + 'tr')

        if page == 1:
            detailRes = requests.get('https://dy.feigua.cn/LiveDetail?' + param, headers=self.headers)
            detailS = etree.HTML(detailRes.text)
            total = detailS.xpath('//*[@id="tab2"]/div/div[3]/div/div[6]/div[1]/span[3]/text()')[0]
            self.singleRatio = sessionRatio / float(total)

        hasData = False
        if len(tr):
            for i in range(len(tr)):
                print(str(page) + '_' + str(i + 1))
                title = s.xpath(prev + 'tr[{}]/td[1]/div/div[2]/div[1]/a/text()'.format(i + 1))
                if len(title):
                    title = title[1]
                    price = s.xpath(prev + 'tr[{}]/td[2]/span/text()'.format(i + 1))[0]
                    times = s.xpath(prev + 'tr[{}]/td[4]/text()'.format(i + 1))
                    saleOn = s.xpath(prev + 'tr[{}]/td[5]/span/span[1]/text()'.format(i + 1))[0]
                    saleOff = s.xpath(prev + 'tr[{}]/td[5]/span/span[2]/text()'.format(i + 1))[0]
                    saleCount = s.xpath(prev + 'tr[{}]/td[6]/span/text()'.format(i + 1))[0].strip()
                    saleVolumn = s.xpath(prev + 'tr[{}]/td[7]/span/text()'.format(i + 1))[0].strip()
                    promotionid = s.xpath(prev + 'tr[{}]/td[1]/div/div[2]/div[1]/a/@data-promotionid'.format(i + 1))[0]
                    ts = s.xpath(prev + 'tr[{}]/td[1]/div/div[2]/div[1]/a/@data-ts'.format(i + 1))[0]
                    sign = s.xpath(prev + 'tr[{}]/td[1]/div/div[2]/div[1]/a/@data-sign'.format(i + 1))[0]

                    detailLink = 'id=' + promotionid + '&gid=&active=hot&timestamp=' + ts + '&signature=' + sign
                    shopName = self.get_shopName(detailLink)

                    pattern = re.compile(r'\r|\n|<br>', re.S)
                    title = pattern.sub('', title).strip()

                    info = [
                        self.name,
                        nickName,
                        startTime,
                        shopName,
                        title,
                        pattern.sub('', price).strip(),
                        pattern.sub('', times[0]).strip(),
                        pattern.sub('', times[1]).strip(),
                        saleOn,
                        saleOff,
                        saleCount,
                        saleVolumn
                    ]
                    self.signal.emit(info, self.singleRatio)

                    hasData = True
        return hasData

    def get_shopName(self, href):
        res = requests.get('https://dy.feigua.cn/GoodsNew/Detail?' + href, headers=self.headers)
        s = etree.HTML(res.text)
        shopName = s.xpath('//dd/text()')
        shopName = shopName[0] if len(shopName) > 0 else 'https://dy.feigua.cn/Member#/GoodsNew/Detail?' + href

        return shopName
