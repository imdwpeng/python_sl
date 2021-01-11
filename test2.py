from PyQt5.Qt import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class FingerTabWidget(QTabBar):
    def __init__(self, *args, **kwargs):
        self.tabSize = QSize(kwargs.pop('width'), kwargs.pop('height'))
        super(FingerTabWidget, self).__init__(*args, **kwargs)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        option = QStyleOptionTab()

        for index in range(self.count()):
            self.initStyleOption(option, index)
            tabRect = self.tabRect(index)
            tabRect.moveLeft(10)
            painter.drawControl(QStyle.CE_TabBarTabShape, option)
            painter.drawText(tabRect, Qt.AlignVCenter |
                             Qt.TextDontClip,
                             self.tabText(index));

    def tabSizeHint(self,index):
        return self.tabSize