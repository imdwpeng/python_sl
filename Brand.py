'''
Author: Dong
Date: 2021-01-04 20:21:54
LastEditors: Dong
LastEditTime: 2021-01-04 22:02:24
'''
import re
import requests
from lxml import etree
from fake_useragent import UserAgent
import time
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from TableView import Table
from WorkerThread import WorkerThread

g_step = 0
header = [
    '店名',
    '类别',
    '链接',
    '产品1',
    '销量1',
    '产品2',
    '销量2',
    '产品3',
    '销量3'
]
checkbox = {
    '护肤': '4',
    '彩妆': '5',
    '日用百货': '6',
    '美食饮品': '13'
}


class Brand:
    def __init__(self):
        names = self.__dict__
        names['layout'] = QVBoxLayout()

        # 搜索栏
        names['form_widget'] = QWidget()
        names['form_layout'] = QFormLayout()
        names['form_layout'].setFormAlignment(Qt.AlignTop)
        # 日期范围
        date = QHBoxLayout()
        names['date_week'] = QRadioButton('周')
        names['date_month'] = QRadioButton('月')
        date.addWidget(names['date_week'])
        date.addWidget(names['date_month'])
        # 小店分类
        product_type = QHBoxLayout()
        names['product_skincare'] = QCheckBox('护肤')
        names['product_makeup'] = QCheckBox('彩妆')
        names['product_daily'] = QCheckBox('日用百货')
        names['product_food'] = QCheckBox('美食饮品')
        product_type.addWidget(names['product_skincare'])
        product_type.addWidget(names['product_makeup'])
        product_type.addWidget(names['product_daily'])
        product_type.addWidget(names['product_food'])
        # 搜索条件添加日期范围、关键词
        names['form_layout'].addRow(QLabel('日期范围'), date)
        names['form_layout'].addRow(QLabel('小店分类'), product_type)
        names['form_widget'].setLayout(names['form_layout'])

        # 按钮栏
        names['btn_widget'] = QWidget()
        names['btn_layout'] = QHBoxLayout()
        # 开始按钮
        names['btn_search'] = QPushButton("开始")
        names['btn_search'].setObjectName('btn_search')
        names['btn_search'].setMinimumWidth(100)
        # 下载按钮
        names['btn_download'] = QPushButton("下载")
        names['btn_download'].setMinimumWidth(100)
        # 按钮栏添加开始、下载按钮
        names['btn_layout'].addStretch(1)
        names['btn_layout'].addWidget(names['btn_search'])
        names['btn_layout'].addWidget(names['btn_download'])
        names['btn_layout'].addStretch(1)
        names['btn_widget'].setLayout(names['btn_layout'])

        # 进度条
        names['process_bar'] = QProgressBar()

        # 主布局添加搜索栏、按钮栏、进度条
        names['layout'].addWidget(names['form_widget'])
        names['layout'].addWidget(names['btn_widget'])
        names['layout'].addWidget(names['process_bar'])

    def init_brand_ui(self):
        # 创建表格
        self.initTable(self.brand)
        self.brand.table_main.setColumnCount(len(header))
        self.brand.table_main.setHorizontalHeaderLabels(header)

        # 主布局添加表格
        self.brand.layout.addWidget(self.brand.table_widget, 10)

        # 初始值
        # 日期选择周
        self.brand.date_week.setChecked(True)
        # 小店分类
        self.brand.product_skincare.setChecked(True)
        self.brand.product_makeup.setChecked(True)
        self.brand.product_daily.setChecked(True)
        self.brand.product_food.setChecked(True)
        # 隐藏下载按钮
        self.brand.btn_download.setVisible(False)
        # 进度条
        self.brand.process_bar.setValue(0)
        self.brand.process_bar.setFixedHeight(20)
        self.brand.process_bar.setVisible(False)

        self.tabs.feigua_brand_widget.setLayout(self.brand.layout)

        # 关联事件
        self.brand.btn_search.clicked.connect(self.search_brand_data)
        self.brand.btn_download.clicked.connect(lambda: self.download(self.brand, '品牌旗舰店', header))

    def search_brand_data(self):
        # 日期范围
        date = 'week' if self.brand.date_week.isChecked() else 'month'

        # 小店分类
        skincare = checkbox[self.brand.product_skincare.text()] if self.brand.product_skincare.isChecked() else ''
        makeup = checkbox[self.brand.product_makeup.text()] if self.brand.product_makeup.isChecked() else ''
        daily = checkbox[self.brand.product_daily.text()] if self.brand.product_daily.isChecked() else ''
        food = checkbox[self.brand.product_food.text()] if self.brand.product_food.isChecked() else ''

        checkbox_list = []

        if skincare:
            checkbox_list.append(skincare)
        if makeup:
            checkbox_list.append(makeup)
        if daily:
            checkbox_list.append(daily)
        if food:
            checkbox_list.append(food)

        # 不存在cookie
        if self.cookie == '':
            return QMessageBox.information(self, '提示', '没有设置登陆信息，请先点击左上角绿色图标设置', QMessageBox.Close)
        elif len(checkbox_list) == 0:
            return QMessageBox.information(self, '提示', '请选择小店类型', QMessageBox.Close)

        # 开始查询
        self.brand.thread = WorkerThread(self.get_search_brand, self.cookie, checkbox_list, date)  # 创建线程
        self.brand.thread.signal.connect(self.update_brand_data)  # 线程连接相关callback事件
        self.brand.thread.start()  # 启动线程

    # 更新数据
    def update_brand_data(self, info, new_step):
        global g_step
        # 初始化数据
        if g_step < 100 and not self.brand.process_bar.isVisible():
            self.brand.table_main.setRowCount(0)
            self.brand.btn_download.setVisible(False)
            self.brand.process_bar.setVisible(True)
            self.brand.process_bar.setValue(0)

            # 置灰按钮
            self.brand.btn_search.setEnabled(False)
            self.change_tabs_type(False)

        step = new_step
        if len(info):
            # 新增表格数据
            self.addRow(self.brand, info)
        else:
            # 没有info时，new_step传的是最终的进度，不是step单元，用于校正进度
            g_step = new_step
            step = 0

        # 更新进度条
        self.set_brand_step(step)

        # 查询完成
        if g_step >= 100:
            # 如果有数据的话，显示下载按钮
            if self.brand.table_main.rowCount():
                self.brand.btn_download.setVisible(True)

            # 重置进度条
            # self.brand.process_bar.setVisible(False)
            # self.brand.process_bar.setValue(0)

            # 恢复按钮
            self.brand.btn_search.setEnabled(True)
            self.change_tabs_type(True)

    # 更新进度条
    def set_brand_step(self, step):
        global g_step
        print(g_step)
        print(step)
        new_step = g_step + step
        if int(g_step) < int(new_step):
            for iStep in range(int(g_step), int(new_step)):
                g_step += 1
                self.brand.process_bar.setValue(g_step)
                time.sleep(0.1)
        g_step = new_step
        self.brand.process_bar.setValue(g_step)

    # =============================================================================
    def get_search_brand(self, cookie, cateId, date, totalRatio):
        pageRatio = totalRatio / float(100)
        self.page = 1
        self.get_page(cookie, cateId, date, pageRatio)

    def get_page(self, cookie, cateId, date, pageRatio):
        print('第' + str(self.page) + '页')
        self.url = "https://dy.feigua.cn/EShop/FlagShipShopRank?sort=TotalOrderAccount&flagShip=1"
        self.headers = {
            "Cookie": cookie
        }

        self.detailUrl = "https://dy.feigua.cn/EShop/ProductAnalysis?ispartial=true&page=1&sort=0&CateId=0"
        print(self.url + "&cateid=" + cateId + "&page=" + str(self.page) + "&period=" + date)
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
                self.brand.thread.signal.emit(info + products, singleRatio)

            print('=======================================')
            time.sleep(0.1)
            if self.page <= 100:
                self.page += 1
                self.get_page(cookie, cateId, date, pageRatio)
        else:
            print("Error！")

        print('=======================================')
        time.sleep(0.1)

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