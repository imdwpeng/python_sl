import sys
import os
import time
import random
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from TableView import Table
from Tabs import Tabs
from Live import Live
from Brand import Brand
import resource  # 将图标资源打包进exe中

brandHeader = [
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

g_step = 0

class MainUi(QMainWindow, Tabs, Live):
    def __init__(self):
        super().__init__()

        # 绝对路径（针对于打包后相对路径错误）
        self.path = os.path.dirname(os.path.dirname(os.path.realpath(sys.executable)))

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.left_widget = QWidget()  # 创建左侧部件
        self.left_layout = QVBoxLayout()  # 创建左侧部件的纵向布局
        self.right_widget = QWidget()  # 创建右侧部件
        self.right_layout = QGridLayout()  # 创建右侧部件的纵向布局
        self.left_bar_widget = QWidget()  # 创建左侧工具栏
        self.left_bar_layout = QHBoxLayout()  # 创建左侧工具栏的横向布局
        self.left_title_widget = QWidget()  # 创建左侧icon栏
        self.left_title_layout = QHBoxLayout()  # 创建左侧icon栏的横向布局
        self.left_tab_widget = QWidget()  # 创建左侧导航栏
        self.left_tab_layout = QGridLayout()  # 创建左侧导航栏的网格布局
        self.left_close = QToolButton()  # 关闭按钮
        self.left_visit = QToolButton()  # 设置按钮
        self.left_mini = QToolButton()  # 最小化按钮
        self.icon = QLabel()  # icon
        self.title = QLabel("小牛爬虫")  # 标题
        self.right_bar_widget = QWidget()  # 创建搜索栏
        self.right_bar_layout = QGridLayout()  # 创建搜索栏的网格布局
        self.date_label = QLabel('日期范围')  # 日期范围
        self.date_week = QRadioButton('周')
        self.date_month = QRadioButton('月')
        self.search_label = QLabel('关键词')  # 搜索标题
        self.right_bar_widget_search_input = QLineEdit()  # 搜索框
        self.brand_label = QLabel('品牌名')  # 品牌名
        self.right_bar_widget_brand_text = QTextEdit()  # 品牌列表
        self.check_skincare = QCheckBox('护肤', self)  # 护肤
        self.check_makeup = QCheckBox('彩妆', self)  # 彩妆
        self.check_daily = QCheckBox('日用百货', self)  # 日用百货
        self.check_food = QCheckBox('美食饮品', self)  # 美食饮品
        self.right_btn_widget = QWidget()  # 创建操作组
        self.right_btn_layout = QHBoxLayout()  # 创建操作组的横向布局
        self.search_btn = QPushButton("开始")  # 搜索按钮
        self.down_btn = QPushButton("下载")  # 下载按钮
        self.right_process_bar = QProgressBar()  # 进度条

        # 绑定事件
        # 关闭窗口
        self.left_close.clicked.connect(self.showCloseDialog)
        # 最小化
        self.left_mini.clicked.connect(self.showMinimized)
        # 显示cookie设置框
        self.left_visit.clicked.connect(self.showCookieDialog)
        
        # 创建tab标签
        self.tabs = Tabs()
        self.live = Live()

        self.init_tabs_ui()
        self.init_live_ui()
        self.init_ui()

        # 初始值
        self.check_skincare.setVisible(False)
        self.check_daily.setVisible(False)
        self.check_makeup.setVisible(False)
        self.check_food.setVisible(False)
        # 先设置cookie
        self.cookie = ''
        self.showCookieDialog()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowIcon(QIcon(':/ox.ico'))  # 设置图标

        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget.setObjectName('left_widget')
        self.left_widget.setLayout(self.left_layout)  # 设置窗口左侧部件布局为网格布局

        self.right_widget.setObjectName('right_widget')
        self.right_widget.setLayout(self.right_layout)  # 设置窗口右侧部件布局为网格布局

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占12行2列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第2列，占12行10列
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_layout.setSpacing(0)

        # 左侧界面
        # 顶部操作栏
        self.left_close.setIcon(QIcon(':/close.ico'))
        self.left_close.setIconSize(QSize(8, 8))
        self.left_mini.setIcon(QIcon(':/minus.ico'))
        self.left_mini.setIconSize(QSize(10, 6))
        self.left_visit.setIcon(QIcon(':/settings.ico'))
        self.left_visit.setIconSize(QSize(12, 12))
        self.left_close.setCursor(Qt.PointingHandCursor)
        self.left_mini.setCursor(Qt.PointingHandCursor)
        self.left_visit.setCursor(Qt.PointingHandCursor)
        self.left_close.setToolTip('关闭')
        self.left_visit.setToolTip('设置')
        self.left_mini.setToolTip('最小化')
        self.left_close.setFixedSize(15, 15)
        self.left_visit.setFixedSize(15, 15)
        self.left_mini.setFixedSize(15, 15)
        
        # icon标题栏
        self.icon.setFixedWidth(30)
        self.icon.setFixedHeight(30)
        self.icon.setScaledContents(True)
        self.icon.setPixmap(QPixmap(':/ox.ico'))

        self.left_bar_widget.setLayout(self.left_bar_layout)
        self.left_title_widget.setLayout(self.left_title_layout)
        self.left_tab_widget.setLayout(self.left_tab_layout)

        self.left_bar_layout.addWidget(self.left_close)
        self.left_bar_layout.addWidget(self.left_mini)
        self.left_bar_layout.addWidget(self.left_visit)
        self.left_bar_layout.addStretch(1)

        self.left_title_layout.addWidget(self.icon)
        self.left_title_layout.addWidget(self.title)

        self.left_layout.addWidget(self.left_bar_widget)
        self.left_layout.addWidget(self.left_title_widget)
        self.left_layout.addWidget(self.left_tab_widget)
        self.left_layout.addStretch(1)

        # 右侧界面
        # 搜索框
        self.right_bar_widget.setLayout(self.right_bar_layout)

        # 日期范围
        self.date_label.setObjectName('label')
        self.date_week.setObjectName('radio')
        self.date_month.setObjectName('radio')
        self.date_week.setChecked(True)

        # 小店分类
        self.search_label.setObjectName('label')
        self.check_skincare.setObjectName('checkbox')
        self.check_makeup.setObjectName('checkbox')
        self.check_daily.setObjectName('checkbox')
        self.check_food.setObjectName('checkbox')
        self.check_skincare.setChecked(True)
        self.check_makeup.setChecked(True)
        self.check_daily.setChecked(True)
        self.check_food.setChecked(True)

        # 关键词搜索
        self.right_bar_widget_search_input.setPlaceholderText("输入播主，逗号隔开")
        # 品牌列表
        self.brand_label.setObjectName('label')
        self.brand_label.setVisible(False)
        self.right_bar_widget_brand_text.setVisible(False)
        self.right_bar_widget_brand_text.setFixedHeight(50)
        self.right_bar_widget_brand_text.setPlaceholderText("输入品牌名，逗号隔开")

        self.right_bar_layout.addWidget(self.date_label, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.date_week, 0, 1, 1, 1)
        self.right_bar_layout.addWidget(self.date_month, 0, 2, 1, 1)
        self.right_bar_layout.addWidget(self.search_label, 1, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 1, 1, 1, 9)
        self.right_bar_layout.addWidget(self.check_skincare, 1, 1, 1, 1)
        self.right_bar_layout.addWidget(self.check_makeup, 1, 2, 1, 1)
        self.right_bar_layout.addWidget(self.check_daily, 1, 3, 1, 1)
        self.right_bar_layout.addWidget(self.check_food, 1, 4, 1, 1)
        self.right_bar_layout.addWidget(self.brand_label, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_brand_text, 0, 1, 1, 9)

        # 操作按钮组
        self.right_btn_widget.setLayout(self.right_btn_layout)
        self.search_btn.setObjectName('search')
        self.search_btn.setMinimumWidth(100)
        self.down_btn.setObjectName("download")
        self.down_btn.setMinimumWidth(100)
        self.down_btn.setVisible(False)
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.down_btn.setCursor(Qt.PointingHandCursor)
        self.right_btn_layout.addStretch(1)
        self.right_btn_layout.addWidget(self.search_btn)
        self.right_btn_layout.addWidget(self.down_btn)
        self.right_btn_layout.addStretch(1)

        # 进度条
        self.right_process_bar.setValue(0)
        self.right_process_bar.setFixedHeight(20)
        self.right_process_bar.setVisible(False)

        # 样式
        randomNum = random.randint(1, 6)
        if randomNum == 1:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/1.png);}''')
        elif randomNum == 2:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/2.png);}''')
        elif randomNum == 3:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/3.png);}''')
        elif randomNum == 4:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/4.png);}''')
        elif randomNum == 5:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/5.png);}''')
        elif randomNum == 6:
            self.left_widget.setStyleSheet('''QWidget#left_widget{border-image: url(:/6.png);}''')
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{
                background-color:#000;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')

        self.left_close.setStyleSheet('''
            QToolButton{
                background:#F76677;
                border-radius:7px;
            }
            QToolButton:hover{
                background:red;
            }
        ''')
        self.left_mini.setStyleSheet('''
            QToolButton{
                background:#F7D674;
                border-radius:7px;
            }
            QToolButton:hover{
                background:yellow;
            }
        ''')
        self.left_visit.setStyleSheet('''
            QToolButton{
                background:#6DDF6D;
                border-radius:7px;
            }
            QToolButton:hover{
                background:green;
            }
        ''')
        self.left_tab_widget.setStyleSheet('''
            QPushButton{
                padding-bottom:5px;
                margin-bottom: 10px;
                border:none;
                color:white;
                text-align:left;
            }
            QPushButton#left_label{
                color:#ddd;
            }
            QPushButton#left_button{
                padding-left:10px;
                height: 30px;
            }
            QPushButton#left_button:hover{
                border-bottom:1px solid blue;
                font-size: 18px;
                font-weight:700;
            }
            QPushButton#left_button:checked{
                border-bottom:1px solid blue;
                font-size: 18px;
                font-weight:700;
            }
        ''')
        self.title.setStyleSheet('''
            QLabel{
                font-weight:500;
                font-size:16px;
                color:#fff;
            }
        ''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                background:#fff;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QTabWidget::pane{
                border:none;
            }
            QTabWidget::tab-bar{
                    alignment:left;
            }
            QTabBar::tab{
                background:transparent;
            }
            QTabBar::tab:hover{
                background:rgb(255, 255, 255, 100);
            }
            QTabBar::tab:selected{
                border-color: white;
                background:white;
                color:green;
            }
            QLabel{
                color:#666;
            }
            QCheckBox{
                color:#000;
            }
            QRadioButton{
                color:#000;
            }
            QLineEdit{
                color:#000;
                background:#fff;
                border:1px solid gray;
                width:300px;
                border-radius:10px;
                padding:2px 4px;
            }
            QLineEdit:focus{
                outline:none;
            }
            QPushButton{
                padding:5px 10px;
                margin:0 10px;
                color:#333;
                background:#ddd;
                border:1px solid #ddd;
                border-radius:4px;
            }
            QPushButton#btn_search{
                color:#fff;
                background:#0170fe;
            }
            QProgressBar{
                border: 2px solid grey;
                border-radius: 5px;
                background-color: #FFFFFF;
                text-align: center;
                color: rgb(255, 85, 0);
            }
            QProgressBar::chunk {
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0170fe, stop:1 #0000FF);
            }
       ''')
       #  self.right_bar_widget_brand_text.setStyleSheet('''
       #      QTextEdit{
       #          color:#000;
       #          background:#fff;
       #          border:1px solid gray;
       #          width:300px;
       #          border-radius:10px;
       #          padding:2px 4px;
       #      }
       #  ''')

    # 二次确认关闭窗口
    def showCloseDialog(self):
        A = QMessageBox.question(self, '提示', '是否确认退出程序？', QMessageBox.Yes | QMessageBox.No)
        if A == QMessageBox.Yes:
            # 退出进程
            if self.thread and self.thread.isRunning and self.thread.isRunning():
                self.thread.quit()
            self.close()

    # 显示cookie框
    def showCookieDialog(self):
        cookie, ok = QInputDialog.getMultiLineText(self, "设置登录信息", "Cookie:", self.cookie)

        if ok:
            self.cookie = cookie

    # 切换数据类型
    def change_tab_callback(self, index):
        print(index)

    # 爬数据
    def searchData(self):
        # 日期范围
        dateList = ['7', '30'] if self.activeTab == '直播红人' else ['week', 'month']
        date = dateList[0] if self.date_week.isChecked() else dateList[1]

        # 直播红人
        keyword = self.right_bar_widget_search_input.text()
        # 品牌旗舰店
        skincare = checkbox[self.check_skincare.text()] if self.check_skincare.isChecked() else ''
        makeup = checkbox[self.check_makeup.text()] if self.check_makeup.isChecked() else ''
        daily = checkbox[self.check_daily.text()] if self.check_daily.isChecked() else ''
        food = checkbox[self.check_food.text()] if self.check_food.isChecked() else ''

        keyword_list = keyword.split('，') if '，' in keyword else keyword.split(',')
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
        # 直播时需要输入关键词
        elif self.activeTab == '直播红人' and keyword == '':
            return QMessageBox.information(self, '提示', '请输入需要搜索的播主', QMessageBox.Close)
        elif self.activeTab == '品牌旗舰店' and len(checkbox_list) == 0:
            return QMessageBox.information(self, '提示', '请选择小店类型', QMessageBox.Close)

        # 开始查询
        search_type = ''
        data_list = []
        global g_step
        g_step = 0
        if self.activeTab == '直播红人' and len(keyword_list):
            search_type = 'live'
            data_list = keyword_list
        elif self.activeTab == '品牌旗舰店' and len(checkbox_list):
            search_type = 'brand'
            data_list = checkbox_list

        if search_type:
            self.thread = Worker(data_list, date, search_type)  # 创建线程
            self.thread.signal.connect(self.update_data)  # 线程连接相关callback事件
            self.thread.start()  # 启动线程

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True

        self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
        event.accept()
        self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
        QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


def main():
    app = QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
