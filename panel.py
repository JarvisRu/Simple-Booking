import sys
from datetime import datetime
import search_train
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSpinBox)

class OrderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        # self.resize(300, 200)
        # self.move(400,200)
        # self.setWindowTitle('Simple Booking')
        
        self.__window_layout = QHBoxLayout()
        self.__setSearchBoxUI()

        self.__window_layout.addWidget(self.__search_box)


        self.setLayout(self.__window_layout)

    def __setSearchBoxUI(self):
        self.__search_box = QGroupBox('Search Section')
        h_box_time = QHBoxLayout()
        h_box_go = QHBoxLayout()
        h_box_back = QHBoxLayout()
        
        local_time = datetime.now()
        self.__year = QSpinBox()
        self.__year.setRange(2018,2021)
        self.__year.setValue(local_time.year)
        self.__year.setStatusTip('Select the year')
        self.__month = QSpinBox()
        self.__month.setRange(1, 12)
        self.__month.setValue(local_time.month)
        self.__month.setStatusTip('Select the month')
        self.__day = QSpinBox()
        self.__day.setRange(1, 31)
        self.__day.setValue(local_time.day)
        self.__day.setStatusTip('Select the day')
        h_box_time.addWidget(self.__year)
        h_box_time.addWidget(self.__month)
        h_box_time.addWidget(self.__day)

        go_text = QLabel('Toucheng to Zongli')
        go_btn = QPushButton('Search', self)
        go_btn.setStatusTip('Search Train for Toucheng to Zongli')
        go_btn.clicked.connect(lambda: self.__search(0))
        h_box_go.addWidget(go_text)
        h_box_go.addStretch(1)
        h_box_go.addWidget(go_btn)

        back_text = QLabel('Zongli to Toucheng')
        back_btn = QPushButton('Search', self)
        back_btn.setStatusTip('Search Train for Zongli to Toucheng')
        back_btn.clicked.connect(lambda: self.__search(1))
        h_box_back.addWidget(back_text)
        h_box_back.addStretch(1)
        h_box_back.addWidget(back_btn)
        
        vBox = QVBoxLayout()
        vBox.addLayout(h_box_time)
        vBox.addLayout(h_box_go)
        vBox.addLayout(h_box_back)
        self.__search_box.setLayout(vBox)

    def __formatTime(slef, time):
        if time >= 1 and time <= 9:
            return '0' + str(time)
        else:
            return str(time)

    @pyqtSlot(int)
    def __search(self, mode):
        year = self.__formatTime(self.__year.value())
        month = self.__formatTime(self.__month.value())
        day = self.__formatTime(self.__day.value())
        search_train.search(mode, year, month, day)

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.move(400,200)
        self.setWindowTitle('Simple Booking')
        self.statusBar()
        self.setCentralWidget(OrderPanel())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = BaseWindow()
    w.show()   
    
    sys.exit(app.exec_())