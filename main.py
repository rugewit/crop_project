import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QDialog, QApplication, QMainWindow, QGraphicsScene, QGraphicsItem, \
    QGraphicsRectItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, QFrame, QLabel, QGraphicsTextItem, QFileDialog, \
    QLineEdit
from PyQt5.QtCore import Qt, QMimeData, QPoint, QRect, QSize, QRectF, QSizeF, QPropertyAnimation, QTimeLine, QObject, \
    QTimer, QTime
from PyQt5.QtGui import QDrag, QImage, QColor, QPen, QBrush, QPaintEvent
from PyQt5 import uic
import random
import winsound
from PyQt5.QtWidgets import (QApplication, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsScene)
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import (QObject, QPointF,
                          QPropertyAnimation, pyqtProperty)
import sys
from PyQt5.uic.properties import QtGui
#import settings
from PyQt5.QtGui import QTransform
import settings
from PIL import Image
import os
import shutil




img = QImage('bg.jpg')
img_path = 'bg.jpg'
mode = 1
x_tmp , y_tmp = (0,0)
#d = 12

class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.has_img = False

    def setImage(self,img):
        self.setPixmap(QPixmap.fromImage(img))
        self.has_img = True

    def paintEvent(self, QPaintEvent):
        global mode,x_tmp , y_tmp
        temp = None
        super().paintEvent(QPaintEvent)
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
        painter = QPainter(self)
        if mode == 2:
            painter.setBrush(QBrush(QColor('white')))
            painter.drawRect(x0,y0,settings.width,settings.height)
            if mode == 3:
                painter.setPen(QPen(QColor('green'), 5, Qt.SolidLine, Qt.RoundCap))
                painter.drawPoint(x_tmp , y_tmp)
                painter.setPen(QPen(QColor('red'), 1, Qt.SolidLine, Qt.RoundCap))
        if self.has_img:
            width = temp.width()
            height = temp.height()
            painter.setPen(QPen(QColor('red'), 1, Qt.SolidLine, Qt.RoundCap))
            for i in range(0, settings.count_x + 1):
                painter.drawLine(x0 + i * width //  settings.count_x, y0,x0 + i * width //  settings.count_x, y0 + height )
            for i in range(0,settings.count_y + 1):
                painter.drawLine(x0 , y0 + i * (height // settings.count_y)  ,x0 + width, y0 + i * (height // settings.count_y)  )


    def mousePressEvent(self, e):
        global mode
        super().mousePressEvent(e)
        x_tmp,y_tmp = e.x(), e.y()
        if 121<=x_tmp<=968 and 94<=y_tmp<=571 and mode == 2:
            i = (x_tmp - 121) // (self.pixmap().width()//settings.count_x)
            y = (y_tmp - 94) // (self.pixmap().height()//settings.count_y)
            x_tmp, y_tmp = i, y
            mode = 3
            self.update()
        self.update()

def initUI(self):
    uic.loadUi('MainWindow.ui', self)
    self.btn_load_img.clicked.connect(self.load_image)
    self.imageLabel = Label()
    self.frame_copy = self.frame
    self.scrollArea.setWidget(self.imageLabel)
    self.imageLabel.setAlignment( Qt.AlignVCenter | Qt.AlignCenter)
    self.btn_confirm.clicked.connect(self.confirm_input)
    self.btn_choose_folder.clicked.connect(self.output_folder)
    self.btn_crop.clicked.connect(self.start_croping)
    self.btn_mode_1.clicked.connect(self.start_mode_1)
    self.btn_mode_2.clicked.connect(self.start_mode_2)


def crop(path,x1, y1, x2, y2,x,y):
    print('сохраняю в '+ path)
    global img,img_path
    im =Image.open(img_path)
    save_at_template = os.path.join(path, '%d-%d.jpg'%(x,y))
    im.crop((x1, y1, x2, y2)).save(save_at_template)


class MainWnd(QMainWindow):
    global img,img_path
    def __init__(self):
        super().__init__()
        initUI(self)
        self.imageLabel.setImage(img)
        settings.width = img.width()
        settings.height = img.height()

    def load_image(self):

        global img,img_path
        fname = None
        fname,_filter = QFileDialog.getOpenFileName(self, 'Open file',
                                            'c:\\', "Image files (*.jpg *.png)")
        if fname != None:
            img = QImage(fname)
            img_path = fname
            settings.width = img.width()
            settings.height = img.height()
            self.imageLabel.setImage(img)
        print('by loading',img)

    def output_folder(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        settings.output_folder = file

    def start_mode_1(self):
        global mode
        mode = 1
        self.imageLabel.update()

    def start_mode_2(self):
        global mode
        print('mode2')
        try:
            mode = 2
            self.imageLabel.update()
            #self.frame_copy.setParent(self.imageLabel)
            self.show_dialog()
        except Exception as e:
            print(e)

    def show_dialog(self):
        self.d = QDialog()
        uic.loadUi('dialog.ui', self.d)
        self.d.setWindowTitle("Dialog")
        self.d.setParent(None)
        self.d.show()

    def confirm_input(self):
        settings.count_x = int(self.lineEdit_x.text())
        settings.count_y = int(self.lineEdit_y.text())
        self.imageLabel.update()


    def start_croping(self):
        global img,img_path
        print(settings.width,settings.height)
        for i in range(settings.count_x):
            for y in range(settings.count_y):
                print('x1:',i*(settings.width//settings.count_x))
                #print('deltax:',(settings.width//settings.count_x))
                print('y1',y*(settings.height//settings.count_y))
                #print('deltay',(settings.height//settings.count_y))
                x2 = (i+1)*(settings.width//settings.count_x)
                y2 = (y+1)*(settings.height//settings.count_y)
                crop(settings.output_folder,i*(settings.width//settings.count_x),y*(settings.height//settings.count_y),
                     x2,y2,i,y)

    def getfile(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    '''
    d = QDialog()
    uic.loadUi('dialog.ui', d)
    d.setWindowTitle("Dialog")
    d.setParent(None)
    '''
    app.exec_()


