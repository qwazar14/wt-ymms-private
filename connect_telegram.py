import uuid

import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

from gui import save_data_to_config, get_data_from_config


def get_tg_chat_id(message: str, offset: int = -1) -> str or None:
    """
    Возвращает идентификатор чата для конкретного сообщения в Telegram API
    :param message: Тескт сообщения для проверки
    :param offset: Смещение для Telegram API
    :return: Идентификатор чата или None
    """
    URL = "https://api.telegram.org/bot"
    TOKEN = "5593316012:AAGqn46oO9QzrjewKERtcjO9KA1UT-ewa0k"
    response = requests.get(f"{URL}{TOKEN}/getUpdates?offset={offset}")

    data = response.json()["result"]
    for update in data:
        if update["message"]:
            if update["message"]["text"] == message:
                return update["message"]["chat"]["id"]


def tg_send_message(bot_message):
    try:
        bot_token = "5593316012:AAGqn46oO9QzrjewKERtcjO9KA1UT-ewa0k"
        bot_chatID = get_data_from_config("bot_chatID")
        send_text = (
            "https://api.telegram.org/bot"
            + bot_token
            + "/sendMessage?chat_id="
            + bot_chatID
            + "&parse_mode=Markdown&text="
            + bot_message
        )

        response = requests.get(send_text)

        return response.json()
    except:
        pass


class Ui_SecondWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.uuid = uuid.uuid4().hex

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(460, 200)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())

        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(460, 200))
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
        MainWindow.setStyleSheet(
            "background-color: rgb(54, 57, 63);\n"
            'font: 8pt "Levenim MT";\n'
            "color: rgb(255, 255, 255);"
        )
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(460, 0))
        self.centralwidget.setMaximumSize(QtCore.QSize(9999, 9999))
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_done = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_done.setGeometry(QtCore.QRect(20, 120, 421, 70))
        self.pushButton_done.setSizePolicy(sizePolicy)
        self.pushButton_done.setStyleSheet(
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
        self.pushButton_done.setObjectName("pushButton_done")

        self.textEdit_uuid = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_uuid.setGeometry(QtCore.QRect(20, 30, 421, 64))
        self.textEdit_uuid.setObjectName("textEdit_uuid")
        self.textEdit_uuid.setReadOnly(True)
        self.textEdit_uuid.setText(self.uuid)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate("MainWindow", "Подключение вывода в Телеграм")
        )
        self.pushButton_done.setText(_translate("MainWindow", "Подключить"))
        self.add_functions()

    def add_functions(self):
        self.pushButton_done.clicked.connect(lambda: self.connect_telegram())

    def connect_telegram(self):
        bot_chatID = get_tg_chat_id(self.uuid)
        if bot_chatID is not None:
            self.pushButton_done.setEnabled(False)
            self.pushButton_done.setText("готово")
            save_data_to_config("bot_chatID", str(bot_chatID))
        else:
            self.pushButton_done.setText("Попробуйте ещё раз...")
