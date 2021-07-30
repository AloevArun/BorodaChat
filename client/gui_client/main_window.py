import sys

import arrow
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QMessageBox

from client.client import HttpClient
from client.gui_client.gui_authentification import Ui_Dialog
from client.gui_client.gui_design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле gui_design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.dialog = QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        self.auth_window = self.dialog.ui

        self.auth_window.RegistButton_2.clicked.connect(self.registration)
        self.auth_window.LoginButton_2.clicked.connect(self.login)

        self.client = HttpClient()
        # self.sendButton.clicked.connect(self.send_message)
        # self.updateButton.clicked.connect(self.update_widget)
        # self.add_messages(self.all_db_messages())  # получаем ВСЕ сообщения при запуске
        # self.check_server_status()

        self.user_nick = None

        self.dialog.exec()

    def registration(self):
        registration_body = {
            "nick": self.auth_window.RegistTextEdit_2.toPlainText(),
            "login": self.auth_window.RegistEmailTextEdit_2.toPlainText(),
            "password": self.auth_window.RegistPasswordTextEdit_2.toPlainText(),
        }

        # assert '' not in registration_body.values(), f'Some fields is empty. {registration_body.values()}'

        self.client.registration(registration_body)
        self.auth_window.RegistButton_2.setEnabled(False)
        self.auth_window.RegistButton_2.setText("Регистрация завершена")

    def login(self):
        login_body = {
            "login": self.auth_window.LoginTextEdit_2.toPlainText(),
            "password": self.auth_window.PasswordTextEdit_2.toPlainText(),
        }
        # assert '' not in login_body.values(), f'Some fields is empty. {login_body.values()}'

        user_data = self.client.login(login_body)
        if not user_data:
            QMessageBox(f'Access denied. Unknown login/password')
            return

        self.user_nick = user_data['nick']
        self.dialog.accept()
        self.UserLabel.setText(self.user_nick)

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
