import os
import re
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# Регулярное выражение для поиска строк с количеством полученных пакетов
received_packages = re.compile(r"(\d) received")
status = ("no response", "alive but losses", "alive")


class PingWorker(threading.Thread):
    def __init__(self, ip, update_ui_callback):
        super().__init__()
        self.ip = ip
        self.update_ui_callback = update_ui_callback

    def run(self):
        # Выполнение команды ping
        ping_out = os.popen(f"ping -q -c2 {self.ip}", "r")
        self.update_ui_callback(f"... pinging {self.ip}")

        # Обработка результата ping
        while True:
            line = ping_out.readline()
            if not line:
                break
            n_received = received_packages.findall(line)
            if n_received:
                # Отправка результата в UI
                result = f"{self.ip}: {status[int(n_received[0])]}"
                self.update_ui_callback(result)


class PingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ping IP Addresses")

        # Создаем текстовое поле для вывода информации
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # Только для чтения

        # Создаем кнопку для запуска пинга
        self.ping_button = QPushButton("Start Ping", self)
        self.ping_button.clicked.connect(self.start_ping)

        # Создаем основной layout
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.ping_button)

        # Устанавливаем виджет в центральную область
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_ping(self):
        # Очищаем текстовое поле
        self.text_edit.clear()

        # Запуск пинга в отдельных потоках
        for suffix in range(20, 30):
            ip = f"192.168.178.{suffix}"
            worker = PingWorker(ip, self.update_ui)
            worker.start()

    def update_ui(self, text):
        # Метод для обновления текстового поля с результатами
        self.text_edit.append(text)


if __name__ == "__main__":
    # Запуск приложения
    app = QApplication(sys.argv)

    window = PingApp()
    window.show()

    sys.exit(app.exec_())
