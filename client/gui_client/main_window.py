import sys
from hashlib import sha256

import arrow
import requests.exceptions
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QMessageBox

from client.gui_client.gui_authentification import Ui_Dialog
from client.gui_client.gui_design import Ui_MainWindow
from client.request_manager import HttpClient


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.dialog = QDialog()
        self.dialog.ui = Ui_Dialog()
        self.dialog.ui.setupUi(self.dialog)

        self.auth_window = self.dialog.ui

        self.auth_window.RegistButton.clicked.connect(self.registration)
        self.auth_window.LoginButton.clicked.connect(self.show_chat)
        self.auth_window.PingButton.clicked.connect(self.check_server_status)

        self.window().UpdateButton.clicked.connect(self.all_db_messages)

        self.client = HttpClient()
        self.user_nick = None
        self.msgbox = QMessageBox()
        self.dialog.exec()
        self.password = ''

    def show_chat(self):
        login = self.auth_window.LoginTextEdit.toPlainText()
        password = str(sha256(self.auth_window.PasswordTextEdit.toPlainText().encode('utf-8')).hexdigest())
        response = self.auth(login, password)
        if response != 'denied':
            self.window().show()
            self.UserLabel.setText(response)
            self.password = password
            self.dialog.close()
        else:
            pass

    def registration(self):
        registration_body = {
            "nickname": self.auth_window.RegistTextEdit.toPlainText(),
            "login": self.auth_window.RegistEmailTextEdit.toPlainText(),
            "password": str(sha256(self.auth_window.RegistPasswordTextEdit.toPlainText().encode('utf-8')).hexdigest())
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
        else:
            self.auth_window.RegistStatusLabel.setText(f'Что-то пошло не так.')
            self.auth_window.RegistStatusLabel.setStyleSheet('color: red')

    def auth(self, login, password):
        credentials = {
            "login": login,
            "password": password,
        }
        response = self.client.login(credentials)
        self.user_nick = response.get('response')

        if self.user_nick == 'denied':
            self.msgbox.setWindowTitle('Сервер')
            self.msgbox.setText("Неверный логин/пароль!")
            self.msgbox.exec()
            return 'denied'
        else:
            return response['response']

    # получение ВСЕХ сообщений из базы
    def all_db_messages(self):
        user = self.UserLabel.text()
        messages = self.client.get_all_messages(user, self.password)
        print(messages)
        return messages

    def update_widget(self):
        time = self.messageList.item(self.messageList.count() - 1).text()
        messages = self.client.update_messages(time)['messages']
        if len(messages) != 0:
            self.add_messages(messages)
            return messages

    # НЕ АКТУАЛЬНО
    # добавление ВСЕХ требуемых сообщений из 'messages_to_add'
    def add_messages(self, messages_to_add: dict) -> None:
        if messages_to_add != 0:
            for message in messages_to_add:
                if message not in self.messageList.selectedItems():
                    self.add_message_to_widget(message)

        self.messageList.scrollToBottom()

    # НЕ АКТУАЛЬНО
    # добавление одного(!) сообщения
    def add_message_to_widget(self, message: dict) -> None:
        msg = message['message']
        user = message['user']
        date = message['time']
        fmt = 'YYYY-MM-DDTh:m:s.SS'
        arw = arrow.get(date, fmt).format(fmt)
        self.messageList.addItem(f'| {arw} | {user}: {msg}')

    # НЕ АКТУАЛЬНО
    # отправляем сообщение и обновляем сообщения с сервера
    # !!!убрать 'update_messages()' и 'check_server_status()' после реализации автоматического обновления
    def send_message(self) -> None:
        if self.userLineEdit.text() != '' and self.messageLineEdit.text() != '':  # если поля не пустые
            text = self.messageLineEdit.text()  # текст сообщения
            self.client.send_message(text, self.user_nick)  # отправляем имя пользователя, сообщение и время
            self.update_widget()  # обновляем сообщения с сервера
            self.messageLineEdit.clear()  # очищаем поле ввода сообщения ('messageLineEdit')
            self.check_server_status()

    # пинг\проверка соединения
    def check_server_status(self):
        host = {
            "ip": self.auth_window.IPTextEdit.toPlainText(),
            "port": self.auth_window.PortTextEdit.toPlainText()
        }
        try:
            self.client.base_url = f'http://{host["ip"]}:{host["port"]}'
            if self.client.check_server()["status"] == 'online':
                self.msgbox.setWindowTitle('Сервер')
                self.msgbox.setText('Соединение с сервером установлено!')
                self.msgbox.exec()
        except requests.exceptions.ConnectionError:
            self.msgbox.setText('Сервер недоступен, проверьте введенный адрес.')
            self.msgbox.exec()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # новый экземпляр QApplication
    window = MainWindow()  # создаём объект класса ExampleApp
    app.exec()  # запускаем движок
