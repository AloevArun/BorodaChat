import sys

import arrow
from PyQt6 import QtWidgets

from client import HttpClient
from client.gui_client import gui_design


class MainWindow(QtWidgets.QMainWindow, gui_design.Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле gui_design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.client = HttpClient()
        self.sendButton.clicked.connect(self.send_message)
        self.updateButton.clicked.connect(self.update_widget)
        self.add_messages(self.all_db_messages())  # получаем ВСЕ сообщения при запуске
        # self.check_server_status()

    def all_db_messages(self):  # возвращает ВСЕ сообщения из базы
        messages = self.client.get_all_messages()['messages']
        return messages

    def update_widget(self):
        time = self.messageList.item(self.messageList.count() - 1).text()
        messages = self.client.update_messages(time)['messages']
        if len(messages) != 0:
            self.add_messages(messages)
            return messages

    def add_messages(self, messages_to_add: dict) -> None:
        if messages_to_add != 0:
            for message in messages_to_add:
                if message not in self.messageList.selectedItems():
                    self.add_message_to_widget(message)

        self.messageList.scrollToBottom()

    # добавление ВСЕХ требуемых сообщений из 'messages_to_add'

    def add_message_to_widget(self, message: dict) -> None:
        msg = message['message']
        user = message['user']
        date = message['time']
        fmt = 'YYYY-MM-DDTh:m:s.SS'
        arw = arrow.get(date, fmt).format(fmt)
        self.messageList.addItem(f'| {arw} | {user}: {msg}')

    # добавление одного(!) сообщения

    def send_message(self) -> None:
        if self.userLineEdit.text() != '' and self.messageLineEdit.text() != '':  # если поля не пустые
            text = self.messageLineEdit.text()  # текст сообщения
            user = self.userLineEdit.text()  # имя пользователя
            self.client.send_message(text, user)  # отправляем имя пользователя, сообщение и время
            self.update_widget()  # обновляем сообщения с сервера
            self.messageLineEdit.clear()  # очищаем поле ввода сообщения ('messageLineEdit')
            self.check_server_status()

    # отправляем сообщение и обновляем сообщения с сервера
    # !!!убрать 'update_messages()' и 'check_server_status()' после реализации автоматического обновления
    def check_server_status(self):
        status = self.client.check_server()
        if status['status'] == 'online':
            self.onlineLabel.setText('Online')
            self.onlineLabel.update()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # новый экземпляр QApplication
    window = MainWindow()  # создаём объект класса ExampleApp
    window.show()  # запускаем интерфейс
    app.exec()  # запускаем движок
