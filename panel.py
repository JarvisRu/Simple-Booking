import sys
import webbrowser
from datetime import datetime
import search_train
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem)

class OrderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.__window_layout = QVBoxLayout()
        self.__setSearchBoxUI()
        self.__setResultBoxUI()
        self.__setBookingBoxUI()

        self.__window_layout.addWidget(self.__search_box)
        self.__window_layout.addWidget(self.__result_box)
        self.__window_layout.addWidget(self.__booking_box)

        self.__window_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__window_layout)

    def __setSearchBoxUI(self):
        self.__search_box = QGroupBox('Search')
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
    
    def __setResultBoxUI(self):
        self.__result_box = QGroupBox('Result')
        
        self.__train_table = QTableWidget()
        self.__train_table.setColumnCount(7)
        self.__train_table.setRowCount(7)
        self.__train_table.setHorizontalHeaderLabels(['Type','Train Code','Via','Departure Time','Arrival Time','Need Time','Money'])

        self.__table_text = QLabel('-')
        self.__table_text.setAlignment(Qt.AlignCenter) 

        vBox = QVBoxLayout()
        vBox.addWidget(self.__table_text)
        vBox.addWidget(self.__train_table)
        self.__result_box.setLayout(vBox)
    
    def __setBookingBoxUI(self):
        self.__booking_box = QGroupBox('Booking')

        book_text = QLabel('Pleas input train code: ')
        self.__book_input = QLineEdit()
        self.__book_input.setStatusTip('Pleas input the train code which you want to buy')
        book_btn = QPushButton('To booking Page', self)
        book_btn.setStatusTip('Opening webbrowser with booking page')
        book_btn.clicked.connect(self.__go_booking)

        hBox = QHBoxLayout()
        hBox.addWidget(book_text)
        hBox.addWidget(self.__book_input)
        hBox.addWidget(book_btn)
        self.__booking_box.setLayout(hBox)
    
    def __updateResultBox(self):
        self.__table_text.setText(self.__now_mode + '  |  ' + self.__search_time)
        self.__train_table.setRowCount(len(self.__train_type))

        for row, train in enumerate(self.__train_type):
            item = QTableWidgetItem(train)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 0, item)
        for row, train_code in enumerate(self.__train_code):
            item = QTableWidgetItem(train_code)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 1, item)
        for row, via in enumerate(self.__via):
            item = QTableWidgetItem(via)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 2, item)
        for row, departure_time in enumerate(self.__departure_time):
            item = QTableWidgetItem(departure_time)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 3, item)
        for row, arrival_time in enumerate(self.__arrival_time):
            item = QTableWidgetItem(arrival_time)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 4, item)
        for row, need_time in enumerate(self.__need_time):
            item = QTableWidgetItem(str(need_time))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 5, item)
        for row, money in enumerate(self.__money):
            item = QTableWidgetItem(str(money))
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsSelectable)
            self.__train_table.setItem(row, 6, item)

    def __formatTime(slef, time):
        if time >= 1 and time <= 9:
            return '0' + str(time)
        else:
            return str(time)

    @pyqtSlot(int)
    def __search(self, mode):
        self.__now_mode = 'Toucheng to Zongli' if mode == 0 else 'Zongli to Toucheng'
        self.__from_station = '077' if mode == 0 else '108'
        self.__to_station = '108' if mode == 0 else '077'
        year = self.__formatTime(self.__year.value())
        month = self.__formatTime(self.__month.value())
        day = self.__formatTime(self.__day.value())
        self.__search_time = year + '/' + month + '/' + day

        self.__train_type, self.__train_code, self.__via, self.__departure_time, self.__arrival_time, self.__need_time, self.__money = search_train.search(mode, year, month, day)
        self.__updateResultBox()
    
    @pyqtSlot()
    def __go_booking(self):
        order_url = "http://railway.hinet.net/Foreign/TW/etno1.html?from_station=" + self.__from_station + "&to_station=" + self.__to_station + "&getin_date=" + self.__search_time + "&train_no=" + self.__book_input.text()
        webbrowser.open(order_url, new=0)

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(630, 405)
        self.move(400,200)
        self.setWindowTitle('Simple Booking')
        self.statusBar()
        self.setCentralWidget(OrderPanel())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = BaseWindow()
    w.show()   

    sys.exit(app.exec_())