import sys  # sys нужен для передачи argv в QApplication
import arrow
from PyQt6 import QtWidgets

from client import HttpClient
from gui_client import gui_design  # Это наш конвертированный файл дизайна


class MainWindow(QtWidgets.QMainWindow, gui_design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.client = HttpClient()
        self.sendButton.clicked.connect(self.send_message)
        self.add_all_messages()

    def add_all_messages(self):
        db_messages = self.client.all_messages()
        unpacked_messages = db_messages['messages']
        for message in unpacked_messages:
            print(message)
            msg = message['message']
            user = message['user']
            date = message['time']
            fmt = 'YYYY-MM-DDTh:m:s.SS'
            arw = arrow.get(date, fmt).format('HH:mm')
            self.messageList.addItem(f'| {arw} | {user}: {msg}')

    # def send_message(self):
    #     text = self.textEdit.toPlainText()
    #     user = self.textEdit2.toPlainText()
    #     self.client.send_message(text, user)
    #

    def send_message(self):
        if self.userLineEdit.text() == '':
            pass
        elif self.messageLineEdit.text() == '':
            pass
        else:
            text = self.messageLineEdit.text()
            user = self.userLineEdit.text()
            self.client.send_message(text, user)
            self.add_message(user, text)
            self.messageLineEdit.clear()

    def add_message(self, user, message_item):
        self.messageList.addItem(f'{user}: {message_item}')

    def type_message(self):
        print(self.text())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
