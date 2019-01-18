import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QFrame, QLabel, QGraphicsTextItem, QFileDialog
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, QSize, QRectF, QSizeF, QPropertyAnimation, QTimeLine, QObject, \
    QTimer, QTime
from PyQt5.QtGui import QDrag, QImage, QColor, QPen, QBrush
from PyQt5 import uic
import random
import winsound
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF,
                          QPropertyAnimation, pyqtProperty)
import sys
# qwe
from PyQt5.uic.properties import QtGui
#import settings
from PyQt5.QtGui import QTransform




img = None

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.has_img = False

    def setImage(self,img):
        self.setPixmap(QPixmap.fromImage(img))
        self.has_img = True

    def paintEvent(self, QPaintEvent):
        super().paintEvent(QPaintEvent)
        try:
            temp = self.pixmap()
            print(temp)
            print(temp.rect())
            print(temp.size())
            x0 = (self.width() - temp.width()) / 2
            y0 = (self.height() - temp.height()) / 2
            if x0 < 0:
                x0 = 0
            if y0 < 0:
                y0 = 0
            print(x0, y0)
        except Exception as e:
            print(e)
        painter = QPainter(self)
        if self.has_img:
            painter.setPen(QPen(QColor('red'), 1, Qt.SolidLine, Qt.RoundCap))
            painter.setBrush(QBrush(QColor('green'), Qt.SolidPattern))

            painter.drawLine(x0, y0, x0 + temp.width(), y0 + temp.height())


def initUI(self):
    uic.loadUi('MainWindow.ui', self)
    self.btn_load_img.clicked.connect(self.load_image)
    self.imageLabel = Label()

    #self.scene = Scene(self.graphicsView.size().width(),self.graphicsView.size().height())

    #self.graphicsView.setScene(self.scene)
    self.scrollArea.setWidget(self.imageLabel)
    self.imageLabel.setAlignment( Qt.AlignVCenter | Qt.AlignCenter)
    #self.setCentralWidget(self.scrollArea)




class MainWnd(QMainWindow):
    def __init__(self):
        super().__init__()
        initUI(self)

    def load_image(self):

        global img
        fname = None
        try:
            fname,_filter = QFileDialog.getOpenFileName(self, 'Open file',
                                                'c:\\', "Image files (*.jpg *.png)")
        except Exception as e:
            print(123)
        if fname != None:
            img = QImage(fname)
            try:
                #self.graphicsView.resize(img.width(),img.height())
                #self.scene.setSceneRect(0, 0, img.width(), img.height())
                self.imageLabel.setImage(img)
            except Exception as e:
                print(e)
        print('by loading',img)





    def getfile(self):
        pass
        #self.le.setPixmap(QPixmap(fname))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    app.exec_()


