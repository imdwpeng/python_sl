'''
Author: Dong
Date: 2021-01-06 09:03:36
LastEditors: Dong
LastEditTime: 2021-01-07 23:08:27
'''
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

tabs = [
    {
        'type': 'feigua',
        'name': '飞瓜',
        'children': [
            {
                'type': 'feigua_live',
                'name': '直播红人',
                'icon': ':/live.svg',
                'defaultChecked': True
            },
            {
                'type': 'feigua_brand',
                'name': '品牌旗舰店',
                'icon': ':/brand.svg',
                'defaultChecked': False
            }
        ]
    },
    {
        'type': 'analysis',
        'name': '数据分析',
        'children': [
            {
                'type': 'analysis_brand',
                'name': '品牌转换',
                'icon': ':/live.svg',
                'defaultChecked': False
            },
        ]
    }
]

class Tabs():
    def __init__(self):
        names = self.__dict__
        names['tab_widget'] = QTabWidget()
        names['tab_widget'].setTabPosition(QTabWidget.West)
        for i in range(len(tabs)):
            names[tabs[i]['type']] = QPushButton(tabs[i]['name'])
            names[tabs[i]['type']].setObjectName('left_label')
            children = tabs[i]['children']
            if len(children):
                for j in range(len(children)):
                    # 创建tab
                    names[children[j]['type'] + '_widget'] = QWidget()
                    names['tab_widget'].addTab(names[children[j]['type'] + '_widget'], children[j]['name'])

                    names[children[j]['type']] = QPushButton(children[j]['name'])
                    names[children[j]['type']].setObjectName('left_button')
                    # 设置图标
                    icon = QIcon()
                    icon.addPixmap(QPixmap(children[j]['icon']))
                    names[children[j]['type']].setIcon(icon)
                    names[children[j]['type']].setIconSize(QSize(12, 12))
                    # 设置鼠标样式
                    names[children[j]['type']].setCursor(Qt.PointingHandCursor)
                    # 让按钮变得只有两种状态：选中/未选中
                    names[children[j]['type']].setCheckable(True)

                    # 默认选中
                    if children[j]['defaultChecked']:
                        names['tab_widget'].setCurrentWidget(names[children[j]['type'] + '_widget'])
                        names[children[j]['type']].setChecked(True) 
    
    def init_tabs_ui(self):
        # 关联点击切换tab事件
        self.tabs.feigua_live.clicked[bool].connect(lambda: self.change_tab(0))
        self.tabs.feigua_brand.clicked[bool].connect(lambda: self.change_tab(1))
        self.tabs.analysis_brand.clicked[bool].connect(lambda: self.change_tab(2))

        # 飞瓜
        self.left_tab_layout.addWidget(self.tabs.feigua, 1, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.feigua_live, 2, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.feigua_brand, 4, 0, 1, 1)
        # 数据分析
        self.left_tab_layout.addWidget(self.tabs.analysis, 6, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.analysis_brand, 7, 0, 1, 1)

        # tab对应的页面
        self.right_layout.addWidget(self.tabs.tab_widget)
    
    # 切换数据类型
    def change_tab(self, index):
        # 初始化按钮状态
        self.tabs.feigua_live.setChecked(False)
        self.tabs.feigua_brand.setChecked(False)
        self.tabs.analysis_brand.setChecked(False)

        # 直播红人
        if index == 0:
            self.tabs.feigua_live.setChecked(True)
        # 品牌旗舰店
        elif index == 1:
            self.tabs.feigua_brand.setChecked(True)
        # 品牌转换
        elif index == 2:
            self.tabs.analysis_brand.setChecked(True)

        self.tabs.tab_widget.setCurrentIndex(index)
