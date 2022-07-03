import configparser

import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal as Signal
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from pynput.keyboard import Listener
from transliterate import translit

import main


def save_data_to_config(key, value):
    """
    Сохраняет значение в конфигурационный файл
    :param key: Ключ
    :param value: Значение
    """
    config = configparser.ConfigParser()
    config_path = "config.ini"
    config.read(config_path)
    config["DEFAULT"][key] = value
    with open(config_path, "w") as configfile:
        config.write(configfile)


def get_data_from_config(key):
    """
    Получает значение из конфигурационного файла
    :param key:
    :return:
    """
    config = configparser.ConfigParser()
    config.read("config.ini")
    data = config["DEFAULT"][key]
    return data



class MyGetPosThread(QThread):
    positionSign = Signal(object)

    def __init__(self, parent):
        QThread.__init__(self, parent)


    def addPositionEventListener(self, listener):
        self.positionSign.connect(listener)

    def on_press(self, key):
        try:
            a = str(key)
        except AttributeError:
            a = str(key)
        if a == get_data_from_config('button'): self.m_pressed = True
        if a != get_data_from_config('button'): self.m_pressed = False

        try:
            if self.m_pressed == True:
                self.positionSign.emit(pyautogui.position())
        except:
            pass


    def run(self):

        with Listener(on_press=self.on_press) as listener:
            listener.join()


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.is_on = False
        self.button_css_default = (
            "QPushButton\n"
            "                                                 {\n"
            "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(189, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
            '                                                 font: 75 13pt \\"Levenim MT\\";\n'
            "                                                 color: rgb(255, 255, 255);\n"
            "                                                 border-radius: 30px\n"
            "                                                 }\n"
            "                                                 QPushButton::hover\n"
            "                                                 {\n"
            "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
            '                                                 font: 75 13pt \\"Levenim MT\\";\n'
            "                                                 color: rgb(255, 255, 255);\n"
            "                                                 border-radius: 30px\n"
            "                                                 }\n"
            "                                                 QPushButton::pressed\n"
            "                                                 {\n"
            "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(0, 0, 0, 255));\n"
            '                                                 font: 75 13pt \\"Levenim MT\\";\n'
            "                                                 color: rgb(255, 255, 255);\n"
            "                                                 border-radius: 30px}"
        )
        self.button_css_unenable = (
            "QPushButton\n"
            "                                                 {\n"
            "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(0, 0, 0, 255));\n"
            '                                                 font: 75 13pt \\"Levenim MT\\";\n'
            "                                                 color: rgb(255, 255, 255);\n"
            "                                                 border-radius: 30px}"
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.progressBar = QtWidgets.QProgressBar(self.frame_2)
        self.pushButton_pathToDir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_connectTG = QtWidgets.QPushButton(self.centralwidget)
        # self.pushButton_startStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clearDic = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_chooseButton = QtWidgets.QPushButton(self.centralwidget)
        self.textEdit_selected_button = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_license_date = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_distance = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_css = ("QTextEdit{ border-radius: 5px; border:0px;background-color: rgba(255, 255, 255, 0);\n"
                             'font: 87 26pt "Arial";}')
        self.path = ""

        self._get_pos_thread = MyGetPosThread(self)
        self._get_pos_thread.addPositionEventListener(self.onPosEvent)
        self._get_pos_thread.start()

    def setupUi(self, main_window):
        """
        Инициализация главного окна
        :param main_window:
        :return:
        """
        main_window.setObjectName("WT-YMMS")
        main_window.resize(460, 465)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())

        main_window.setSizePolicy(sizePolicy)
        main_window.setMinimumSize(QtCore.QSize(460, 400))
        main_window.setMaximumSize(QtCore.QSize(460, 400))
        main_window.setSizeIncrement(QtCore.QSize(0, 0))

        font = QtGui.QFont()
        font.setFamily("Levenim MT")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)

        main_window.setFont(font)
        main_window.setMouseTracking(True)
        main_window.setStyleSheet(
            "background-color: rgb(54, 57, 63);\n"
            'font: 8pt "Levenim MT";\n'
            "color: rgb(255, 255, 255);"
        )
        main_window.setTabShape(QtWidgets.QTabWidget.Rounded)

        # self.centralwidget.setEnabled(True)
        # self.centralwidget.setSizePolicy(sizePolicy)
        # self.centralwidget.setMinimumSize(QtCore.QSize(800, 0))
        # self.centralwidget.setMaximumSize(QtCore.QSize(9999, 9999))
        # self.centralwidget.setObjectName("centralwidget")

        self.frame_2.setGeometry(QtCore.QRect(100, 549, 701, 51))
        self.frame_2.setStyleSheet("background-color: rgb(32, 34, 37);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.pushButton_pathToDir.setGeometry(QtCore.QRect(240, 150, 200, 70))
        self.pushButton_pathToDir.setSizePolicy(sizePolicy)
        self.pushButton_pathToDir.setFont(font)
        self.pushButton_pathToDir.setStyleSheet(self.button_css_default)
        self.pushButton_pathToDir.setObjectName("pushButton_pathToDir")

        self.pushButton_connectTG.setGeometry(QtCore.QRect(20, 150, 200, 70))
        self.pushButton_connectTG.setSizePolicy(sizePolicy)
        self.pushButton_connectTG.setStyleSheet(self.button_css_unenable)
        self.pushButton_connectTG.setObjectName("pushButton_connectTG")
        self.pushButton_connectTG.setEnabled(False)
        # self.pushButton_startStop.setGeometry(QtCore.QRect(20, 130, 421, 70))
        # self.pushButton_startStop.setSizePolicy(sizePolicy)
        # self.pushButton_startStop.setStyleSheet(self.button_css_default)
        # self.pushButton_startStop.setObjectName("pushButton_startStop")

        self.pushButton_clearDic.setGeometry(QtCore.QRect(20, 240, 200, 70))
        self.pushButton_clearDic.setSizePolicy(sizePolicy)
        self.pushButton_clearDic.setStyleSheet(self.button_css_unenable)
        self.pushButton_clearDic.setObjectName("pushButton_clearDic")
        self.pushButton_clearDic.setEnabled(False)

        self.pushButton_chooseButton.setGeometry(QtCore.QRect(240, 240, 200, 70))
        self.pushButton_chooseButton.setSizePolicy(sizePolicy)
        self.pushButton_chooseButton.setStyleSheet(self.button_css_default)
        self.pushButton_chooseButton.setObjectName("pushButton_chooseButton")

        self.textEdit_selected_button.setEnabled(False)
        self.textEdit_selected_button.setGeometry(QtCore.QRect(240, 330, 201, 51))
        self.textEdit_selected_button.setFont(font)
        self.textEdit_selected_button.setStyleSheet(self.textEdit_css)
        self.textEdit_selected_button.setObjectName("textEdit_selected_button")

        self.textEdit_license_date.setEnabled(False)
        self.textEdit_license_date.setGeometry(QtCore.QRect(20, 330, 201, 51))
        self.textEdit_license_date.setFont(font)
        self.textEdit_license_date.setStyleSheet(self.textEdit_css)
        self.textEdit_license_date.setObjectName("textEdit_license_date")

        self.textEdit_distance.setGeometry(QtCore.QRect(190, 40, 104, 64))
        self.textEdit_distance.setStyleSheet(self.textEdit_css)
        self.textEdit_distance.setObjectName("textEdit_distance")
        self.textEdit_distance.setEnabled(False)

        main_window.setCentralWidget(self.centralwidget)
        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        """
        Переводит все названия в текст приложения
        :param main_window:
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("WT-YMMS", "WT-YMMS"))
        self.pushButton_pathToDir.setText(_translate("WT-YMMS", "Путь к папке"))
        self.pushButton_connectTG.setText(_translate("WT-YMMS", "Вывод в ТГ"))
        # self.pushButton_startStop.setText(_translate("WT-YMMS", "Старт"))
        self.pushButton_clearDic.setText(_translate("WT-YMMS", "Очистить папку"))
        self.pushButton_chooseButton.setText(_translate("WT-YMMS", "Настроить кнопку"))
        try:
            self.textEdit_selected_button.setPlaceholderText(
                _translate("WT-YMMS", get_data_from_config("button"))
            )
        except:
            pass

        self.add_functions()

    def add_functions(self):
        """
        Добавляет функции к кнопкам
        :return:
        """
        # self.pushButton_startStop.clicked.connect(lambda: self.start_app())
        self.pushButton_pathToDir.clicked.connect(lambda: self.openFileNameDialog())
        self.pushButton_chooseButton.clicked.connect(lambda: self.choose_button())


    # def start_app(self):
    #     self.enableButtons(self.is_on)
    #     try:
    #         self.enableButtons(self.is_on)
    #         if not self.is_on:
    #             res = main.main()
    #             self.textEdit_distance.setText(str(res))
    #             self.is_on = True
    #         else:
    #             self.is_on = False
    #
    #     except:
    #         self.pushButton_startStop.setEnabled(False)
    #         self.pushButton_startStop.setStyleSheet(self.button_css_unenable)
    #         self.enableButtons(True)
    #         self.pushButton_startStop.setText("Неверный путь к папке")

    def onPosEvent(self):
        res = main.main()
        self.textEdit_distance.setText(str(res))

    def openFileNameDialog(self):
        """
        Открывает диалоговое окно для выбора папки
        :return:
        """
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        path = str(
            QFileDialog.getExistingDirectory(
                None, "Выберите папку War Thunder", "", options=options
            )
        )
        if path:
            self.path = path
            save_data_to_config("game_path", path)
            # self.pushButton_startStop.setEnabled(True)
            # self.pushButton_startStop.setStyleSheet(self.button_css_default)
            # self.pushButton_startStop.setText("Старт")

    def choose_button(self):
        def on_press(key):
            print("{0} pressed".format(key))
            save_data_to_config("button", str(key))
            return False

        with Listener(on_press=on_press, on_release=None) as listener:
            listener.join()
        self.textEdit_selected_button.setText(get_data_from_config("button"))
        self.textEdit_selected_button.setAlignment(QtCore.Qt.AlignCenter)

    def enableButtons(self, param):
        self.pushButton_chooseButton.setEnabled(param)
        self.pushButton_pathToDir.setEnabled(param)
        self.pushButton_connectTG.setEnabled(param)
        self.pushButton_clearDic.setEnabled(param)
        if param:
            # self.pushButton_startStop.setText("Старт")
            self.pushButton_chooseButton.setStyleSheet(self.button_css_default)
            self.pushButton_pathToDir.setStyleSheet(self.button_css_default)
            self.pushButton_connectTG.setStyleSheet(self.button_css_default)
            self.pushButton_clearDic.setStyleSheet(self.button_css_default)
        else:
            self.textEdit_distance.setText("")
            # self.pushButton_startStop.setText("Стоп")
            self.pushButton_chooseButton.setStyleSheet(self.button_css_unenable)
            self.pushButton_pathToDir.setStyleSheet(self.button_css_unenable)
            self.pushButton_connectTG.setStyleSheet(self.button_css_unenable)
            self.pushButton_clearDic.setStyleSheet(self.button_css_unenable)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
