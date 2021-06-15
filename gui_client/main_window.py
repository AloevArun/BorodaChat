import sys  # sys нужен для передачи argv в QApplication

import arrow
from PyQt6 import QtWidgets

from client import HttpClient
from gui_client import gui_design  # Это наш конвертированный файл дизайна


class MainWindow(QtWidgets.QMainWindow, gui_design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле gui_design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.client = HttpClient()
        self.sendButton.clicked.connect(self.send_message)
        self.updateButton.clicked.connect(self.update_messages)
        self.add_messages(self.get_all_messages())

    def get_all_messages(self):
        messages = self.client.get_all_messages()
        print(messages)
        return messages.json()

    def update_messages(self):
        if self.messageList.count() != 0:
            time = self.messageList.currentItem()[2:23]
            print(time)
            messages = self.client.send_last_message_time(time)
        else:
            messages = self.get_all_messages()
        return messages.json()

    def add_messages(self, all_messages):
        self.messageList.clear()
        messages = all_messages['messages']
        for message in messages:
            if message not in self.messageList.selectedItems():
                print(message)
                msg = message['message']
                user = message['user']
                date = message['time']
                fmt = 'YYYY-MM-DDTh:m:s.SS'
                arw = arrow.get(date, fmt).format(fmt)
                self.messageList.addItem(f'| {arw} | {user}: {msg}')
        self.messageList.scrollToBottom()

    #    def send_message(self):
    #        text = self.textEdit.toPlainText()
    #        user = self.textEdit2.toPlainText()
    #        self.client.send_message(text, user)

    def send_message(self):
        if self.userLineEdit.text() != '' or self.messageLineEdit.text() != '':
            text = self.messageLineEdit.text()
            user = self.userLineEdit.text()
            self.client.send_message(text, user)
            self.messageLineEdit.clear()
            self.update_messages()

#    def add_message(self, user, message_item):
#        self.messageList.addItem(f'{user}: {message_item}')

#    def type_message(self):
#        print(self.text())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
