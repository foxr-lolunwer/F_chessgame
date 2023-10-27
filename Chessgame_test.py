import sys

from PyQt6.QtGui import QFont, QPixmap, QPainter, QImage
from PyQt6.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication, QLabel)

import code_copy as code


class MainMenu(QWidget):

    def __init__(self, parent=None):
        super(MainMenu, self).__init__(parent)

        self.label = None
        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 530, 636)
        menu_mainimage = QPixmap()
        qimg = QImage('resource/img/menu_main_bg.png')  # 讀取圖片
        menu_mainimage = menu_mainimage.fromImage(qimg)  # 將圖片加入 QPixmap 物件中
        self.label.setPixmap(menu_mainimage)  # 將 QPixmap 物件加入到 label 裡

        btn = QPushButton('start game', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(380, 175)

        btn = QPushButton('course', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(380, 280)

        btn = QPushButton('setting', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(380, 385)

        btn = QPushButton('exit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(380, 490)

        self.setGeometry(200, 200, 1060, 636)
        self.setMinimumSize(1060, 636)
        self.setMaximumSize(1060, 636)
        self.setWindowTitle('Tooltips')

        self.show()
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap("./resource/img/menu_main_bg.png")
    #     #绘制窗口背景，平铺到整个窗口，随着窗口改变而改变
    #     painter.drawPixmap(self.rect(), pixmap)


def main():

    app = QApplication(sys.argv)
    ex = MainMenu()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
