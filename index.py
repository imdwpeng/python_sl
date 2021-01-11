import sys
import os
import random
from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Tabs import Tabs
from Live import Live
from Brand import Brand
import resource  # 将图标资源打包进exe中


class MainUi(QMainWindow, Tabs, Live, Brand):
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
        self.brand = Brand()

        self.init_tabs_ui()
        self.init_live_ui()
        self.init_brand_ui()
        self.init_ui()

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
                width:0;
                background:transparent;
                color:transparent;
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

    # 二次确认关闭窗口
    def showCloseDialog(self):
        A = QMessageBox.question(self, '提示', '是否确认退出程序？', QMessageBox.Yes | QMessageBox.No)
        if A == QMessageBox.Yes:
            os._exit(0)

    # 显示cookie框
    def showCookieDialog(self):
        cookie, ok = QInputDialog.getMultiLineText(self, "设置登录信息", "Cookie:", self.cookie)

        if ok:
            self.cookie = cookie

    def change_tabs_type(self, status):
        self.tabs.feigua_live.setEnabled(status)
        self.tabs.feigua_brand.setEnabled(status)
        self.tabs.analysis_brand.setEnabled(status)

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
