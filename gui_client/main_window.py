import sys  # sys нужен для передачи argv в QApplication

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
        messages = self.client.all_messages()
        # for msg in messages:
        #     self.listWidget(msg)

    # def send_message(self):
    #     text = self.textEdit.toPlainText()
    #     user = self.textEdit2.toPlainText()
    #     self.client.send_message(text, user)
    #     self.listWidget.addItem(f'{user}: {text}')

    def send_message(self):
        text = self.messageLineEdit
        self.client.send_message(text, 'Betal')

    def delete_text(self):
        self.messageLineEdit.clear()

    def type_message(self):
        print(self.text())


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение
