from PyQt5.Qt import *


class WorkerThread(QThread):
    signal = pyqtSignal(list, float)

    def __init__(self, search, cookie, list, date):
        super().__init__()
        self.search = search
        self.cookie = cookie
        self.list = list
        self.date = date

    def run(self):
        ratio = 100 / float(len(self.list))
        for i in range(len(self.list)):
            self.search(self.cookie, self.list[i], self.date, ratio)

            self.signal.emit([], ratio * (i + 1))
