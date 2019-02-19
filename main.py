import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QColor, QPen, QBrush
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QPixmap
import sys
import settings
from PIL import Image
import os

img = QImage('bg.jpg')
img_path = 'bg.jpg'
# моды нужны для различной отрисовки в paintEvent()
mode = 1
# текущие координаты щелчка мыши
curX, curY = (0, 0)
# текущая ячейка на поле через номер строки и столбца
curRow, curColumn = (0, 0)


# класс ,отвечающий за окно для редактирования
class TunDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('dialog.ui', self)
        self.setWindowTitle("Dialog")
        self.btn_dial_print.clicked.connect(self.start_print_text)

    def start_print_text(self):
        pass


# класс ,отвечающий за вывод картинки (или белого фона) с последующими линиями
class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.has_img = False

    def setImage(self, img):
        self.setPixmap(QPixmap.fromImage(img))
        self.has_img = True

    def paintEvent(self, QPaintEvent):
        global mode, curX, curY
        super().paintEvent(QPaintEvent)
        width = settings.width
        height = settings.height
        x0 = (self.width() - width) // 2
        y0 = (self.height() - height) // 2
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        painter = QPainter(self)
        if mode == 2:
            painter.setBrush(QBrush(QColor('white')))
            painter.drawRect(x0, y0, settings.width, settings.height)
        #отображение текста на ячейке.На будущее
        if mode == 3:
            painter.setBrush(QBrush(QColor('white')))
            painter.drawRect(x0, y0, settings.width, settings.height)
            painter.setPen(QPen(QColor('green'), 5, Qt.SolidLine, Qt.RoundCap))
            painter.drawText(x0 + curRow * width // settings.count_x, y0 + curColumn * height // settings.count_y,
                             'Здесь')
            painter.setPen(QPen(QColor('red'), 1, Qt.SolidLine, Qt.RoundCap))
        if self.has_img:
            painter.setPen(QPen(QColor('red'), 1, Qt.SolidLine, Qt.RoundCap))
            for i in range(0, settings.count_x + 1):
                painter.drawLine(x0 + i * width // settings.count_x, y0, x0 + i * width // settings.count_x,
                                 y0 + height)
            for i in range(0, settings.count_y + 1):
                painter.drawLine(x0, y0 + i * (height // settings.count_y), x0 + width,
                                 y0 + i * (height // settings.count_y))

    def mousePressEvent(self, e):
        pass
        #заготовка на будущее
        '''
        global mode, curX, curY, curRow, curColumn
        super().mousePressEvent(e)
        curX, curY = e.x(), e.y()
        # смотрим ,попал ли щелчёк в картинку и определяем ячейку по столбу и строке
        if 121 <= curX <= 968 and 94 <= curY <= 571 and mode in (2, 3):
            i = (curX - 121) // (self.pixmap().width() // settings.count_x)
            y = (curY - 94) // (self.pixmap().height() // settings.count_y)
            curRow, curColumn = (i, y)
            mode = 3
            self.update()
        self.update()
        '''

# инициализация графических элементов
def initUI(self):
    uic.loadUi('MainWindow.ui', self)
    self.btn_load_img.clicked.connect(self.load_image)
    self.imageLabel = Label()
    self.scrollArea.setWidget(self.imageLabel)
    self.imageLabel.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
    self.btn_confirm.clicked.connect(self.confirm_input)
    self.btn_choose_folder.clicked.connect(self.output_folder)
    self.btn_crop.clicked.connect(self.start_croping)
    self.btn_mode_1.clicked.connect(self.start_mode_1)
    self.btn_mode_2.clicked.connect(self.start_mode_2)


# разрезание фотографии
def crop(path, x1, y1, x2, y2, x, y):
    # print('сохраняю в ' + path)
    global img, img_path
    im = Image.open(img_path)
    save_at_template = os.path.join(path, '%d-%d.jpg' % (x, y))
    im.crop((x1, y1, x2, y2)).save(save_at_template)


class MainWnd(QMainWindow):
    global img, img_path

    def __init__(self):
        super().__init__()
        initUI(self)
        self.imageLabel.setImage(img)
        # ширина и высота картинки
        settings.width = img.width()
        settings.height = img.height()

    def load_image(self):
        global img, img_path
        fname, _filter = QFileDialog.getOpenFileName(self, 'Open file',
                                                     'c:\\', "Image files (*.jpg *.png)")
        if fname is not None:
            img = QImage(fname)
            img_path = fname
            settings.width = img.width()
            settings.height = img.height()
            self.imageLabel.setImage(img)

    def output_folder(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        settings.output_folder = file

    def start_mode_1(self):
        global mode
        mode = 1
        # нужен для перерисовки Label'a
        self.imageLabel.update()

    def start_mode_2(self):
        global mode
        mode = 2
        self.imageLabel.update()
        self.show_dialog()

    # окно для редактирования ячейки
    def show_dialog(self):
        self.dialog = TunDialog()
        self.dialog.show()

    # количество разрезаний по х , у
    def confirm_input(self):
        settings.count_x = int(self.lineEdit_x.text())
        settings.count_y = int(self.lineEdit_y.text())
        self.imageLabel.update()

    # начать разрезание
    def start_croping(self):
        global img, img_path
        for i in range(settings.count_x):
            for y in range(settings.count_y):
                x2 = (i + 1) * (settings.width // settings.count_x)
                y2 = (y + 1) * (settings.height // settings.count_y)
                crop(settings.output_folder, i * (settings.width // settings.count_x),
                     y * (settings.height // settings.count_y),
                     x2, y2, i, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWnd()
    ex.show()
    app.exec_()
