
import sys
from tkinter import CENTER
from tkinter.font import BOLD
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        txt1 = QLabel("한결컴퓨터학원 출석체크 프로그램")
        txt1.setAlignment(Qt.AlignCenter)
        txt1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn1 = QPushButton('회원등록', self)
        btn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        btn2 = QPushButton('출석체크', self)
        btn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #메인화면
        txtbox = QHBoxLayout()
        txtbox.addWidget(txt1)
        btnbox = QHBoxLayout()
        btnbox.addWidget(btn1)
        btnbox.addWidget(btn2)
        
        
        #레이아웃 추가
        layout = QVBoxLayout()
        layout.addLayout(txtbox)
        layout.addLayout(btnbox)

        self.setLayout(layout)
        

        self.setWindowTitle('QPushButton')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
