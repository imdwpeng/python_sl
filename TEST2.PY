
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QDockWidget, QPushButton, QApplication, QWidget, QHBoxLayout, QTabWidget
 
 
class DockDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.docker1 = QDockWidget('Docker1', self)
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.btn1 = QPushButton('btn1')
        self.btn2 = QPushButton('btn2')
        self.btn1.clicked.connect(self.btn1fun)
        self.btn2.clicked.connect(self.btn2fun)
        self.docker1.setWidget(self.btn1)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docker1)
        self.hbox1 = QHBoxLayout()
        self.hbox1.addWidget(self.btn1)
        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.btn2)
        self.widget1 = QWidget()
        self.widget1.setLayout(self.hbox1)
        self.widget2 = QWidget()
        self.widget2.setLayout(self.hbox2)
        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.widget1, 'tab1')
        self.tabwidget.addTab(self.widget2, 'tab2')
        self.docker1.setWidget(self.tabwidget)
        self.setWindowTitle('QTabWidget例子')
        self.resize(400, 300)

        # self.tabwidget.setCurrentIndex(1)
        self.tabwidget.setStyleSheet('''
            QTabBar::tab {width: 0; color: transparent;}
        ''')
 
    def btn1fun(self):
        self.textEdit.setText('btn1')
 
    def btn2fun(self):
        self.textEdit.setText('btn2')
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DockDemo()
    demo.show()
    sys.exit(app.exec_())
