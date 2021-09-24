import json.decoder
import sys
import requests.exceptions

from hashlib import sha256
from PyQt6.QtCore import QThread
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QDialog, QMessageBox
from client.gui_client.gui_authentification import Ui_Dialog
from client.gui_client.gui_design import Ui_MainWindow
from client.gui_client.client import HttpClient


class User:
    login = ''
    password = ''
    nickname = ''

    def set_login(self, login: str):
        self.login = login

    def set_password(self, password: str):
        self.password = password

    def set_nickname(self, nickname: str):
        self.nickname = nickname


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.color = QtGui.QColor()
        self.dialog = QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        self.auth_window = self.dialog.ui

        self.auth_window.RegistButton.clicked.connect(self.registration)
        self.auth_window.LoginButton.clicked.connect(self.show_chat)
        self.auth_window.PingButton.clicked.connect(self.check_server_status)

        self.window().SendButton.clicked.connect(self.send_message)
        self.window().UpdateButton.clicked.connect(self.update_messages_widget)

        self.UserList.itemClicked.connect(self.update_messages_widget)
        self.user = User()
        self.client = HttpClient()
        self.client.base_url = (f'http://{self.auth_window.IPTextEdit.toPlainText()}:'
                                f'{self.auth_window.PortTextEdit.toPlainText()}')
        self.msgbox = QMessageBox()
        self.dialog.exec()


    def show_chat(self):
        self.user.login = self.auth_window.LoginTextEdit.toPlainText()
        self.user.password = \
            str(sha256(self.auth_window.PasswordTextEdit.toPlainText().encode('utf-8')).hexdigest())

        assert '' not in (self.user.login, self.user.password), f'Some Field is Empty'

        user = {
            "login": self.user.login,
            "password": self.user.password
        }
        try:
            response = self.client.login(user)['response']
            if response != 'denied':
                self.window().show()
                self.UserLabel.setText(response)
                MainWindow._user = response
                self.dialog.hide()
                try:
                    messages = self.all_db_messages()
                    if list(messages.keys())[0] == 'response':
                        if messages['response'] == 'no_messages':
                            self.msgbox.information(self, 'Внимание', 'К сожалению, для вас пока нет сообщений.')
                        if messages['response'] == 'dict_error':
                            self.msgbox.critical(self, 'Ошибка', 'Ошибка сервера.')
                except json.decoder.JSONDecodeError:
                    self.msgbox.critical(self, 'Ошибка', 'Некорректные данные!')
                else:
                    self.update_users_widget()
                    self.UserList.setCurrentRow(0)
                    self.update_messages_widget()
            else:
                self.msgbox.critical(self, 'Ошибка', 'Пользователь с указанными данными не зарегистрирован!')
        except all:
            raise Exception('Ошибка авторизации')

    def all_db_messages(self):
        messages = self.client.get_messages(self.user.login, self.user.password)
        return messages

    def get_users(self):
        users = self.client.get_users(self.user.login, self.user.password)
        return users

    def registration(self):
        try:
            self.client.check_server()
        except requests.exceptions.ConnectionError:
            self.msgbox.setWindowTitle('Сервер')
            self.msgbox.setText('Ошибка подключения к серверу!')
            self.msgbox.exec()
        else:
            registration_body = {
                "nickname": self.auth_window.RegistTextEdit.toPlainText(),
                "login": self.auth_window.RegistEmailTextEdit.toPlainText(),
                "password": str(
                    sha256(self.auth_window.RegistPasswordTextEdit.toPlainText().encode('utf-8')).hexdigest())
            }

            assert '' not in registration_body.values(), f'Some fields is empty. {registration_body.values()}'

            response = self.client.registration(registration_body)['response']

            if response == 'added':
                self.auth_window.RegistStatusLabel.setText(f'Пользователь успешно зарегистрирован.')
                self.auth_window.RegistStatusLabel.setStyleSheet('color: green')
            elif response == 'user_exists':
                self.auth_window.RegistStatusLabel.setText(f'Пользователь с таким логином уже зарегистрирован!')
                self.auth_window.RegistStatusLabel.setStyleSheet('color: red')
            elif response == 'nickname_exists':
                self.auth_window.RegistStatusLabel.setText(f'Пользователь с таким ником уже зарегистрирован!')
                self.auth_window.RegistStatusLabel.setStyleSheet('color: red')

    def update_users_widget(self):
        self.UserList.clear()
        self.UserList.addItem(f'Глобальный чат')
        users = self.client.get_users(self.user.login, self.user.password)
        if len(users) != 0:
            for user in users:
                if user != self._user:
                    self.UserList.addItem(user)
        self.UserList.setCurrentRow(0)

    def update_messages_widget(self):
        messages = []
        times = []
        if self.UserList.currentItem().text() != 'Глобальный чат':
            guest = self.UserList.currentItem().text()
        else:
            guest = 'global_chat'
        user_messages = self.client.get_messages(self.user.login, self.user.password)
        if guest in user_messages:
            for message in user_messages[guest]:
                message_to_add = f'{message["sender"]}: {message["message"]}'
                time_to_add = f'{message["time"]}'
                messages.append(message_to_add)
                times.append(time_to_add)
            if messages:
                while self.MessageTable.rowCount() > 0:
                    self.MessageTable.removeRow(0)
                self.add_user_messages(messages, times)
        else:
            while self.MessageTable.rowCount() > 0:
                self.MessageTable.removeRow(0)

    def add_user_messages(self, messages, times) -> None:
        if messages != 0 and times != 0:
            for i in range(len(messages)):
                self.MessageTable.insertRow(i)
                self.MessageTable.setItem(i, 0, QtWidgets.QTableWidgetItem(times[i]))
                self.MessageTable.setItem(i, 1, QtWidgets.QTableWidgetItem(messages[i]))
                self.MessageTable.item(i, 1).setToolTip(messages[i])
        self.MessageTable.scrollToBottom()

    def send_message(self) -> None:
        if self.MessageLineEdit.text() != '':
            text = self.window().MessageLineEdit.text()
            if self.UserList.currentItem().text() == 'Глобальный чат':
                receiver = 'global_chat'
            else:
                receiver = self.UserList.currentItem().text()
            self.client.send_message(self.user.login, self.user.password, receiver, text)
            self.update_messages_widget()
            self.window().MessageLineEdit.clear()

    def check_server_status(self):
        self.client.base_url = (f'http://{self.auth_window.IPTextEdit.toPlainText()}:'
                                f'{self.auth_window.PortTextEdit.toPlainText()}')

        if self.client.base_url == '':
            raise Exception('EmptyField')

        try:
            self.client.check_server()

        except ConnectionError:
            self.msgbox.critical(self, 'Сервер', 'Ошибка подключения к серверу!')

        else:
            self.msgbox.information(self, 'Сервер', 'Соединение установлено!')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    app.exec()
