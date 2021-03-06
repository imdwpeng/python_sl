'''
Author: Dong
Date: 2021-01-06 09:03:36
LastEditors: Dong
LastEditTime: 2021-01-06 09:20:48
'''
import sys
import os
import time
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from  openpyxl import  *

class Table():
    def initTable(self):
        self.table_widget = QWidget()  # 创建表格部件
        self.table_widget.setObjectName('table_widget')
        self.table_layout = QHBoxLayout()  # 创建表格部件的横向布局
        self.table_widget.setLayout(self.table_layout)  # 设置窗口表格部件布局为横向布局

        # 实现的效果是一样的，四行三列，所以要灵活运用函数，这里只是示范一下如何单独设置行列
        self.table_main = QTableWidget()
        self.table_layout.addWidget(self.table_main)

    # 新增行数据
    def addRow(self, info):
        cur_total_row = self.table_main.rowCount()  # 获取表格总行数
        cur_row = cur_total_row + 1
        self.table_main.setRowCount(cur_row)  # 增加一行
        if len(info):
            for i in range(len(info)):
                self.table_main.setItem(cur_total_row, i, QTableWidgetItem(info[i]))
        else:
            print('没有需要添加的数据')
        self.table_main.scrollToBottom()

    # 导出为excel
    def download(self):
        # 实例化
        wb = Workbook()
        # 获取表
        ws = wb.get_sheet_by_name(wb.get_sheet_names()[0])
        # 添加表头
        ws.append(self.tableHeader)

        rowCount = self.table_main.rowCount()
        columnCount = self.table_main.columnCount()
        for i in range(rowCount):
            for j in range(columnCount):
                if self.table_main.item(i, j):
                    data = self.table_main.item(i, j).text()  # 得出tablewidget每行每列的数据
                    ws.cell(row=i+2, column=j+1, value=data)
        # 保存
        filename = './' + self.activeTab + '_' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.xlsx'
        wb.save(filename)
        print('保存成功')
        prev_path = os.getcwd()

        # mac系统
        if 'darwin' in sys.platform:
            subprocess.run(['open', filename], check=True)
        else:
            # win系统
            shellArg = '/e,/select,' + prev_path + '\\' + filename[2:]
            print(shellArg)
            subprocess.run(['Explorer', shellArg])
