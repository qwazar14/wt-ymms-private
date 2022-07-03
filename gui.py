import configparser

import pynput as pynput
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QPushButton
from pynput.keyboard import Key, Listener

import main


def save_data_to_config(key, value):
    """
    Сохраняет значение в конфигурационный файл
    :param key: Ключ
    :param value: Значение
    """
    config = configparser.ConfigParser()
    config_path = 'config.ini'
    config.read(config_path)
    config['DEFAULT'][key] = value
    with open(config_path, 'w') as configfile:
        config.write(configfile)


def get_data_from_config(key):
    """
    Получает значение из конфигурационного файла
    :param key:
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    data = config['DEFAULT'][key]
    return data


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Инициализация главного окна
        :param MainWindow:
        :return:
        """
        MainWindow.setObjectName("WT-YMMS")
        MainWindow.resize(460, 465)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(460, 465))
        MainWindow.setMaximumSize(QtCore.QSize(460, 465))
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Levenim MT")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(False)
        MainWindow.setFont(font)
        MainWindow.setMouseTracking(True)
        MainWindow.setStyleSheet("background-color: rgb(54, 57, 63);\n"
                                 "font: 8pt \"Levenim MT\";\n"
                                 "color: rgb(255, 255, 255);")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.button_css = ("QPushButton\n"
                           "                                                 {\n"
                           "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(189, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
                           "                                                 font: 75 13pt \\\"Levenim MT\\\";\n"
                           "                                                 color: rgb(255, 255, 255);\n"
                           "                                                 border-radius: 30px\n"
                           "                                                 }\n"
                           "                                                 QPushButton::hover\n"
                           "                                                 {\n"
                           "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(255, 0, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
                           "                                                 font: 75 13pt \\\"Levenim MT\\\";\n"
                           "                                                 color: rgb(255, 255, 255);\n"
                           "                                                 border-radius: 30px\n"
                           "                                                 }\n"
                           "                                                 QPushButton::pressed\n"
                           "                                                 {\n"
                           "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(0, 0, 0, 255));\n"
                           "                                                 font: 75 13pt \\\"Levenim MT\\\";\n"
                           "                                                 color: rgb(255, 255, 255);\n"
                           "                                                 border-radius: 30px}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(6)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(800, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(9999, 9999))
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(100, 549, 701, 51))
        self.frame_2.setStyleSheet("background-color: rgb(32, 34, 37);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.progressBar = QtWidgets.QProgressBar(self.frame_2)
        self.progressBar.setGeometry(QtCore.QRect(10, 10, 681, 33))
        self.progressBar.setStyleSheet("font: 12pt \"Levenim MT\";\n"
                                       "")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.pushButton_pathToDir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pathToDir.setGeometry(QtCore.QRect(240, 220, 200, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_pathToDir.sizePolicy().hasHeightForWidth())
        self.pushButton_pathToDir.setSizePolicy(sizePolicy)

        self.pushButton_pathToDir.setFont(font)
        self.pushButton_pathToDir.setStyleSheet(self.button_css)
        self.pushButton_pathToDir.setObjectName("pushButton_pathToDir")
        self.pushButton_conncectTG = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_conncectTG.setGeometry(QtCore.QRect(20, 220, 200, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_conncectTG.sizePolicy().hasHeightForWidth())
        self.pushButton_conncectTG.setSizePolicy(sizePolicy)
        self.pushButton_conncectTG.setStyleSheet(self.button_css)
        self.pushButton_conncectTG.setObjectName("pushButton_conncectTG")
        self.pushButton_startStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_startStop.setGeometry(QtCore.QRect(20, 130, 421, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_startStop.sizePolicy().hasHeightForWidth())
        self.pushButton_startStop.setSizePolicy(sizePolicy)
        self.pushButton_startStop.setStyleSheet(self.button_css)
        self.pushButton_startStop.setObjectName("pushButton_startStop")
        self.pushButton_clearDic = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clearDic.setGeometry(QtCore.QRect(20, 310, 200, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_clearDic.sizePolicy().hasHeightForWidth())
        self.pushButton_clearDic.setSizePolicy(sizePolicy)
        self.pushButton_clearDic.setStyleSheet(self.button_css)
        self.pushButton_clearDic.setObjectName("pushButton_clearDic")
        self.pushButton_chooseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_chooseButton.setGeometry(QtCore.QRect(240, 310, 200, 70))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_chooseButton.sizePolicy().hasHeightForWidth())
        self.pushButton_chooseButton.setSizePolicy(sizePolicy)
        self.pushButton_chooseButton.setStyleSheet(self.button_css)
        self.pushButton_chooseButton.setObjectName("pushButton_chooseButton")
        self.textEdit_selected_button = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_selected_button.setEnabled(False)
        self.textEdit_selected_button.setGeometry(QtCore.QRect(240, 400, 201, 51))

        self.textEdit_selected_button.setFont(font)
        self.textEdit_selected_button.setStyleSheet(
            "QTextEdit{ border-radius: 5px; border:0px;background-color: rgba(255, 255, 255, 0);\n"
            "font: 20pt \"Arial\";}")
        self.textEdit_selected_button.setObjectName("textEdit_selected_button")
        self.textEdit_selected_button.setAlignment(QtCore.Qt.AlignCenter)
        self.textEdit_license_date = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_license_date.setEnabled(False)
        self.textEdit_license_date.setGeometry(QtCore.QRect(20, 400, 201, 51))
        self.textEdit_license_date.setFont(font)
        self.textEdit_license_date.setStyleSheet(
            "QTextEdit{ border-radius: 5px; border:0px;background-color: rgba(255, 255, 255, 0);\n"
            "font: 87 26pt \"Arial\";}")
        self.textEdit_license_date.setObjectName("textEdit_license_date")
        self.textEdit_distance = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_distance.setGeometry(QtCore.QRect(190, 40, 104, 64))
        self.textEdit_distance.setStyleSheet(
            "QTextEdit{ border-radius: 5px; border:0px;background-color: rgba(255, 255, 255, 0);\n"
            "font: 87 26pt \"Arial\";}")
        self.textEdit_distance.setObjectName("textEdit_distance")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.path = ""
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Переводит все названия в текст приложения
        :param MainWindow:
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("WT-YMMS", "WT-YMMS"))
        self.pushButton_pathToDir.setText(_translate("WT-YMMS", "Путь к папке"))
        self.pushButton_conncectTG.setText(_translate("WT-YMMS", "Вывод в ТГ"))
        self.pushButton_startStop.setText(_translate("WT-YMMS", "Старт"))
        self.pushButton_clearDic.setText(_translate("WT-YMMS", "Очистить папку"))
        self.pushButton_chooseButton.setText(_translate("WT-YMMS", "Настроить кнопку"))
        self.textEdit_selected_button.setHtml(_translate("WT-YMMS",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Arial\'; font-size:26pt; font-weight:80; font-style:normal;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Levenim MT\'; font-size:12pt; font-weight:400;\">F12</span></p></body></html>"))
        self.textEdit_selected_button.setPlaceholderText(_translate("WT-YMMS", "http://icanhazip.com"))
        self.textEdit_license_date.setHtml(_translate("WT-YMMS",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'Arial\'; font-size:26pt; font-weight:80; font-style:normal;\">\n"
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Levenim MT\'; font-size:7pt; font-weight:400;\">Действительно до </span><span style=\" font-family:\'Levenim MT\'; font-size:7pt; font-weight:400; text-decoration: underline;\">03.07.2022</span></p></body></html>"))
        self.textEdit_license_date.setPlaceholderText(_translate("WT-YMMS", "http://icanhazip.com"))
        self.textEdit_distance.setHtml(_translate("WT-YMMS",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'Arial\'; font-size:26pt; font-weight:80; font-style:normal;\">\n"
                                                  "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Levenim MT\'; font-size:8pt; font-weight:400;\"></span></p></body></html>"))
        self.textEdit_distance.setEnabled(False)

        self.add_functions()

    def add_functions(self):
        """
        Добавляет функции к кнопкам
        :return:
        """
        self.pushButton_startStop.clicked.connect(lambda: self.set_distance())
        self.pushButton_pathToDir.clicked.connect(lambda: self.openFileNameDialog())
        self.pushButton_chooseButton.clicked.connect(lambda: self.choose_button())

    def set_distance(self):
        """
        Выводит дистанцию от метки игрока до желтой метки
        :return:
        """
        try:
            res = main.main()
            self.textEdit_distance.setText(str(res))
        except:
            self.pushButton_startStop.setEnabled(False)
            self.pushButton_startStop.setStyleSheet("QPushButton\n"

                                                    "                                                 {\n"
                                                    "                                                 background-color: qradialgradient(spread:pad, cx:0.495, cy:0.432136, radius:1.469, fx:0.092, fy:0.130136, stop:0 rgba(107, 107, 107, 255), stop:1 rgba(0, 0, 0, 255));\n"
                                                    "                                                 font: 75 13pt \\\"Levenim MT\\\";\n"
                                                    "                                                 color: rgb(255, 255, 255);\n"
                                                    "                                                 border-radius: 30px}")
            self.pushButton_startStop.setText("Неверный путь к папке")

    def openFileNameDialog(self):
        """
        Открывает диалоговое окно для выбора папки
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = str(QFileDialog.getExistingDirectory(None, "Select Directory", "", options=options))
        if path:
            self.path = path
            save_data_to_config('game_path', path)
            self.pushButton_startStop.setEnabled(True)
            self.pushButton_startStop.setStyleSheet(self.button_css)
            self.pushButton_startStop.setText("Старт")

    def choose_button(self):
        def on_press(key):
            print('{0} pressed'.format(
                key))
            save_data_to_config('button', str(key))
            return False

        with Listener(
                on_press=on_press,
                on_release=None) as listener:
            listener.join()
        self.textEdit_selected_button.setText(get_data_from_config('button'))
        self.textEdit_selected_button.setAlignment(QtCore.Qt.AlignCenter)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
