import sys
import requests.exceptions

from hashlib import sha256
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QDialog, QMessageBox

from gui_client.gui_authentification import Ui_Dialog
from gui_client.gui_design import Ui_MainWindow
from client.requester import HttpClient


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

    # инициализация объектов и логики чата

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.auth_window = QDialog()  # объект взаимодействия с окном авторизации
        self.auth_window.ui = Ui_Dialog()
        self.auth_window.ui.setupUi(self.auth_window)

        self.auth_widget = self.auth_window.ui  # объект взаимодействия с элементами окна авторизации

        # логика элементов окна авторизации
        self.auth_widget.RegistButton.clicked.connect(self.registration)
        self.auth_widget.LoginButton.clicked.connect(self.init_chat)
        self.auth_widget.PingButton.clicked.connect(self.check_server_status)

        # логика элементов главного окна(чата)
        self.SendButton.clicked.connect(self.send_message)
        self.UpdateButton.clicked.connect(self.update_messages_widget)
        self.LogoutButton.clicked.connect(self.logout)
        self.UserList.itemClicked.connect(self.update_messages_widget)

        self.user = User()  # объект хранения пользовательской информации
        self.client = HttpClient()  # объект HTTP запросов
        self.color = QtGui.QColor()  # объект для работы с цветом
        self.msgbox = QMessageBox()  # объект выдачи уведомлений
        self.auth_window.exec()  # запуск окна авторизации

    # ОКНО ЧАТА
    # инициализация данных и чата

    def init_chat(self):
        self.user.login = self.auth_widget.LoginTextEdit.toPlainText()
        self.user.password = self.encrypt(self.auth_widget.PasswordTextEdit.toPlainText())

        assert '' not in (self.user.login, self.user.password), f'Some Field is Empty'

        user = {
            "login": self.user.login,
            "password": self.user.password
        }
        response = self.client.login(user)['response']
        if response != 'denied':
            self.auth_window.hide()
            self.user.nickname = response
            self.UserLabel.setText(response)
            self.show()
            self.update_users_widget()
            self.UserList.setCurrentRow(0)
            self.update_messages_widget()
        else:
            self.msgbox.critical(self, 'Ошибка', 'Некорректные данные пользователя!')

    #

    def all_db_messages(self) -> dict:
        messages = self.client.get_messages(self.user.login, self.user.password)
        return messages

    def get_users(self) -> list:
        users = self.client.get_users(self.user.login, self.user.password)
        return users

    def registration(self) -> None:
        try:
            self.client.check_server()
        except requests.exceptions.ConnectionError:
            self.msgbox.setWindowTitle('Сервер')
            self.msgbox.setText('Ошибка подключения к серверу!')
            self.msgbox.exec()
        else:
            registration_body = {
                "nickname": self.auth_widget.RegistTextEdit.toPlainText(),
                "login": self.auth_widget.RegistEmailTextEdit.toPlainText(),
                "password": self.encrypt(self.auth_widget.RegistPasswordTextEdit.toPlainText())
            }

            assert '' not in registration_body.values(), f'Some fields is empty. {registration_body.values()}'

            response = self.client.registration(registration_body)['response']

            if response == 'added':
                self.auth_widget.RegistStatusLabel.setText(f'Пользователь успешно зарегистрирован.')
                self.auth_widget.RegistStatusLabel.setStyleSheet('color: green')
            elif response == 'user_exists':
                self.auth_widget.RegistStatusLabel.setText(f'Пользователь с таким логином уже зарегистрирован!')
                self.auth_widget.RegistStatusLabel.setStyleSheet('color: red')
            elif response == 'nickname_exists':
                self.auth_widget.RegistStatusLabel.setText(f'Пользователь с таким ником уже зарегистрирован!')
                self.auth_widget.RegistStatusLabel.setStyleSheet('color: red')

    def update_users_widget(self) -> None:
        self.UserList.clear()
        self.UserList.addItem(f'Глобальный чат')
        users = self.client.get_users(self.user.login, self.user.password)
        if len(users) != 0:
            for user in users:
                if user != self.user.nickname:
                    self.UserList.addItem(user)
        self.UserList.setCurrentRow(0)

    def update_messages_widget(self) -> None:
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

    def check_server_status(self) -> None:
        self.client.base_url = (f'http://{self.auth_widget.IPTextEdit.toPlainText()}:'
                                f'{self.auth_widget.PortTextEdit.toPlainText()}')

        if self.client.base_url == '':
            raise Exception('EmptyField')

        try:
            self.client.check_server()

        except ConnectionError:
            self.msgbox.critical(self, 'Сервер', 'Ошибка подключения к серверу!')

        else:
            self.msgbox.information(self, 'Сервер', 'Соединение установлено!')

    def logout(self) -> None:
        self.window().close()
        self.auth_widget.LoginTextEdit.clear()
        self.auth_widget.PasswordTextEdit.clear()
        self.auth_window.show()
        self.auth_widget.IPTextEdit.setFocus()
        self.auth_widget.LoginTextEdit.setFocus()

    @staticmethod
    def encrypt(string: str) -> str:
        return sha256(string.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    app.exec()
