import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QPushButton)

class orderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.__initUI()

    def __initUI(self):
        self.resize(300, 200)
        self.move(400,200)
        self.setWindowTitle('Simple Booking')
        
        self.__window_layout = QHBoxLayout()
        self.__set_search_box()

        self.__window_layout.addWidget(self.__search_box)
        self.setLayout(self.__window_layout)

    def __set_search_box(self):
        self.__search_box = QGroupBox('Search Section')
        h_box_go = QHBoxLayout()
        go_text = QLabel('Toucheng to Zongli')
        go_btn = QPushButton('Search', self)
        go_btn.clicked.connect(lambda: self.__search(0))
        h_box_go.addWidget(go_text)
        h_box_go.addStretch(1)
        h_box_go.addWidget(go_btn)

        h_box_back = QHBoxLayout()
        back_text = QLabel('Zongli to Toucheng')
        back_btn = QPushButton('Search', self)
        back_btn.clicked.connect(lambda: self.__search(1))
        h_box_back.addWidget(back_text)
        h_box_back.addStretch(1)
        h_box_back.addWidget(back_btn)

        vBox = QVBoxLayout()
        vBox.addLayout(h_box_go)
        vBox.addLayout(h_box_back)
        self.__search_box.setLayout(vBox)
    
    def __search(self, mode):
        print(mode)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = orderPanel()
    w.show()
    sys.exit(app.exec_())