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
import time
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from TableView import Table
from WorkerThread import WorkerThread

g_step = 0
header = [
    '主播名',
    '直播间名称',
    '开播时间',
    '店铺名',
    '商品',
    '券后价',
    '上架时间',
    '下架时间',
    '上架销量',
    '下架销量',
    '销量(预估)',
    '销售额(预估)'
]


class Live(Table):
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
        # 关键词
        names['search_input'] = QLineEdit()
        names['search_input'].setFixedWidth(620)
        # 搜索条件添加日期范围、关键词
        names['form_layout'].addRow(QLabel('日期范围'), date)
        names['form_layout'].addRow('关键词', names['search_input'])
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

    def init_live_ui(self):
        # 创建表格
        self.initTable(self.live)
        self.live.table_main.setColumnCount(len(header))
        self.live.table_main.setHorizontalHeaderLabels(header)

        # 主布局添加表格
        self.live.layout.addWidget(self.live.table_widget, 10)

        # 初始值
        # 日期选择周
        self.live.date_week.setChecked(True)
        # 隐藏下载按钮
        self.live.btn_download.setVisible(False)
        # 进度条
        self.live.process_bar.setValue(0)
        self.live.process_bar.setFixedHeight(20)
        self.live.process_bar.setVisible(False)

        self.tabs.feigua_live_widget.setLayout(self.live.layout)

        # 关联事件
        self.live.btn_search.clicked.connect(self.search_live_data)
        self.live.btn_download.clicked.connect(lambda: self.download(self.live, '直播红人', header))

    def search_live_data(self):
        # 日期范围
        date = '7' if self.live.date_week.isChecked() else '30'
        # 直播红人
        keyword = self.live.search_input.text()

        keyword_list = keyword.split('，') if '，' in keyword else keyword.split(',')

        # 不存在cookie
        if self.cookie == '':
            return QMessageBox.information(self, '提示', '没有设置登陆信息，请先点击左上角绿色图标设置', QMessageBox.Close)
        # 需要输入关键词
        elif keyword == '':
            return QMessageBox.information(self, '提示', '请输入需要搜索的播主', QMessageBox.Close)

        # 开始查询
        self.live.thread = WorkerThread(self.get_search_live, self.cookie, keyword_list, date)  # 创建线程
        self.live.thread.signal.connect(self.update_live_data)  # 线程连接相关callback事件
        self.live.thread.start()  # 启动线程

    # 更新数据
    def update_live_data(self, info, new_step):
        global g_step
        # 初始化数据
        if g_step < 100 and not self.live.process_bar.isVisible():
            self.live.table_main.setRowCount(0)
            self.live.btn_download.setVisible(False)
            self.live.process_bar.setVisible(True)
            self.live.process_bar.setValue(0)

            # 置灰按钮
            self.live.btn_search.setEnabled(False)
            self.change_tabs_type(False)

        step = new_step
        if len(info):
            # 新增表格数据
            self.addRow(self.live, info)
        else:
            # 没有info时，new_step传的是最终的进度，不是step单元，用于校正进度
            g_step = new_step
            step = 0

        # 更新进度条
        self.set_live_step(step)

        # 查询完成
        if g_step >= 100:
            # 如果有数据的话，显示下载按钮
            if self.live.table_main.rowCount():
                self.live.btn_download.setVisible(True)

            # 重置进度条
            self.live.process_bar.setVisible(False)
            self.live.process_bar.setValue(0)

            # 恢复按钮
            self.live.btn_search.setEnabled(True)
            self.change_tabs_type(True)

    # 更新进度条
    def set_live_step(self, step):
        global g_step
        new_step = g_step + step
        if int(g_step) < int(new_step):
            for iStep in range(int(g_step), int(new_step)):
                g_step += 1
                self.live.process_bar.setValue(g_step)
                time.sleep(0.1)
        g_step = new_step

    # =============================================================================
    # 数据查询
    def get_search_live(self, cookie, keyword, date, totalRatio):
        self.name = ''
        self.uid = ''
        self.singleRatio = 0
        self.searchUrl = "https://dy.feigua.cn/home/search"
        self.url = "https://dy.feigua.cn/Blogger/LiveAnalysis?page=1&uid="
        self.ua = UserAgent()
        self.headers = {
            "Cookie": cookie,
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
                    self.live.thread.signal.emit(info, self.singleRatio)

                    hasData = True
        return hasData

    def get_shopName(self, href):
        res = requests.get('https://dy.feigua.cn/GoodsNew/Detail?' + href, headers=self.headers)
        s = etree.HTML(res.text)
        shopName = s.xpath('//dd/text()')
        shopName = shopName[0] if len(shopName) > 0 else 'https://dy.feigua.cn/Member#/GoodsNew/Detail?' + href

        return shopName