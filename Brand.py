"""
@Author: Eric
@Date: 2020-07-14 20:39:33
LastEditors: Dong
LastEditTime: 2020-12-29 22:19:42
"""
import re
import requests
import time
from lxml import etree
from PyQt5.QtWidgets import QApplication


class Brand:
    def get_search_brand(self, cateId, date, totalRatio):
        pageRatio = totalRatio / float(100)
        self.page = 1
        self.get_page(cateId, date, pageRatio)

    def get_page(self, cateId, date, pageRatio):
        print('第' + str(self.page) + '页')
        self.url = "https://dy.feigua.cn/EShop/FlagShipShopRank?sort=TotalOrderAccount"
        self.headers = {
            "Cookie": self.cookie
        }

        self.detailUrl = "https://dy.feigua.cn/EShop/ProductAnalysis?ispartial=true&page=1&sort=0&CateId=0"

        res = requests.get(self.url + "&cateid=" + cateId + "&page=" + str(self.page) + "&period=" + date, headers=self.headers)
        s = etree.HTML(res.text)
        prev = '//*[@id="js-promotion-container"]/' if self.page == 1 else '//'
        tr = s.xpath(prev + 'tr')

        if len(tr):
            singleRatio = pageRatio / float(len(tr))
            for i in range(len(tr)):
                name = s.xpath(prev + 'tr[{}]/td[2]/div/div[2]/div[1]/a/text()'.format(i + 1))[0]
                shopId = s.xpath(prev + 'tr[{}]/td[2]/div/div[2]/div[1]/a/@data-shopid'.format(i + 1))[0]
                type_list = s.xpath(prev + 'tr[{}]/td[2]/div/div[2]/div[2]/span'.format(i + 1))
                products = self.get_top3(shopId)
                ype_attr = []
                if len(type_list):
                    for j in range(len(type_list)):
                        type_name = s.xpath(prev + 'tr[{}]/td[2]/div/div[2]/div[2]/span[{}]/text()'.format(i + 1, j + 1))[0]
                        ype_attr.append(type_name)
                info = [
                    name,
                    ','.join(ype_attr),
                    'https://haohuo.jinritemai.com/views/shop/index?id=' + shopId
                ]
                self.addRow(info + products)
                self.setStep(self.step + singleRatio)

            print('=======================================')
            time.sleep(1)
            if self.page <= 100:
                self.page += 1
                self.get_page(cateId, date, pageRatio)
        else:
            print("Error！")

        print('=======================================')
        time.sleep(1)

    def get_top3(self, shopId):
        res = requests.get(self.detailUrl + '&shopId=' + shopId, headers=self.headers)
        s = etree.HTML(res.text)
        trs = s.xpath('//tr')
        products = []
        count = 3 if len(trs) >= 3 else len(trs)
        if count:
            for i in range(count):
                name = s.xpath('//tr[{}]/td[2]/div/div[2]/div[1]/text()'.format(i + 1))[1]
                sale = s.xpath('//tr[{}]/td[6]/text()'.format(i + 1))[0]
                pattern = re.compile(r'\s|\n|<br>', re.S)
                name = pattern.sub('', name)
                products.append(name)
                products.append(sale)
        else:
            print("Error！")
            
        return products