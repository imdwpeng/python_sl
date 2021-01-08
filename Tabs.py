'''
Author: Dong
Date: 2021-01-06 09:03:36
LastEditors: Dong
LastEditTime: 2021-01-07 23:08:27
'''
import sys
import os
import time
import subprocess
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from  openpyxl import  *

tabs = [
    {
        'type': 'tab_feigua',
        'name': '飞瓜',
        'children': [
            {
                'type': 'tabpanel_feigua_live',
                'name': '直播红人',
                'icon': ':/live.svg',
                'defaultChecked': True
            },
            {
                'type': 'tabpanel_feigua_brand',
                'name': '品牌旗舰店',
                'icon': ':/brand.svg',
                'defaultChecked': False
            }
        ]
    },
    {
        'type': 'tab_analysis',
        'name': '数据分析',
        'children': [
            {
                'type': 'tabpanel_analysis_brand',
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
        for i in range(len(tabs)):
            names[tabs[i]['type']] = QPushButton(tabs[i]['name'])
            names[tabs[i]['type']].setObjectName('left_label')
            children = tabs[i]['children']
            if len(children):
                for j in range(len(children)):
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
                
                    if children[j]['defaultChecked']:
                        names[children[j]['type']].setChecked(True) 
    
    def initTabs(self):
        # 默认选中直播红人
        self.activeTab = '直播红人'  

        # 关联点击切换tab事件
        self.tabs.tabpanel_feigua_live.clicked[bool].connect(self.changeTab)
        self.tabs.tabpanel_feigua_brand.clicked[bool].connect(self.changeTab)
        self.tabs.tabpanel_analysis_brand.clicked[bool].connect(self.changeTab)

        # 飞瓜
        self.left_tab_layout.addWidget(self.tabs.tab_feigua, 1, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.tabpanel_feigua_live, 2, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.tabpanel_feigua_brand, 4, 0, 1, 1)
        # 数据分析
        self.left_tab_layout.addWidget(self.tabs.tab_analysis, 6, 0, 1, 1)
        self.left_tab_layout.addWidget(self.tabs.tabpanel_analysis_brand, 7, 0, 1, 1)
    
    # 切换数据类型
    def changeTab(self):
        source = self.sender()
        type = source.text()
        
        # 初始化按钮状态
        self.tabs.tabpanel_feigua_live.setChecked(False)
        self.tabs.tabpanel_feigua_brand.setChecked(False)

        self.activeTab = type
        if type == '直播红人':
            self.tabs.tabpanel_feigua_live.setChecked(True)
        elif type == '品牌旗舰店':
            self.tabs.tabpanel_feigua_brand.setChecked(True)
        
        self.change_tab_callback()