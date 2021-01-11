from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from test2 import FingerTabWidget

import sys

app = QApplication(sys.argv)
tabs = QTabWidget()
tabs.setTabBar(FingerTabWidget(width=100,height=25))
digits = ['Thumb','Pointer','Rude','Ring','Pinky']
for i,d in enumerate(digits):
    widget =  QLabel("Area #%s <br> %s Finger"% (i,d))
    tabs.addTab(widget, d)
tabs.setTabPosition(QTabWidget.West)
tabs.show()
sys.exit(app.exec_())