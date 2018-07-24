import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

class orderPael(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 200)
        self.move(400,200)
        self.setWindowTitle('Simple Booking')

        hBox1 = QHBoxLayout()
        goText = QLabel('Toucheng to Zongli')
        goBtn = QPushButton('Search', self)
        hBox1.addStretch(1)
        hBox1.addWidget(goText)
        hBox1.addStretch(1)
        hBox1.addWidget(goBtn)

        hBox2 = QHBoxLayout()
        backText = QLabel('Zongli to Toucheng')
        backBtn = QPushButton('Search', self)
        hBox2.addStretch(1)
        hBox2.addWidget(backText)
        hBox2.addStretch(1)
        hBox2.addWidget(backBtn)

        vBox = QVBoxLayout()
        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        self.setLayout(vBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = orderPael()
    w.show()
    sys.exit(app.exec_())