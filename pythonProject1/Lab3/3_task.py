import sys
import asyncio
from concurrent.futures import FIRST_COMPLETED
from collections import namedtuple
import aiohttp
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

# Определяем структуру сервиса и список сервисов
Service = namedtuple('Service', ('name', 'url', 'ip_attr'))

SERVICES = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)

# Асинхронная функция для получения IP от одного сервиса
async def fetch_ip(service):
    async with aiohttp.ClientSession() as session:
        async with session.get(service.url) as response:
            data = await response.json()
            return data[service.ip_attr]

# Основная асинхронная функция для запуска задач
async def asynchronous():
    tasks = [asyncio.create_task(fetch_ip(service)) for service in SERVICES]

    # Ждем выполнения хотя бы одной задачи
    done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)

    for task in done:
        try:
            ip = task.result()
            return ip  # Возвращаем IP-адрес
        except Exception as e:
            print(f"Error fetching IP: {e}")

    # Отменяем остальные задачи, которые ещё не завершены
    for task in pending:
        task.cancel()


# Класс для выполнения асинхронной задачи в отдельном потоке
class IPFetcher(QThread):
    finished = pyqtSignal(str)  # Сигнал, который будет отправлен после получения IP

    def run(self):
        try:
            ip = asyncio.run(asynchronous())  # Запуск асинхронной задачи
            self.finished.emit(ip)  # Отправляем результат через сигнал
        except Exception as e:
            self.finished.emit(f"Error: {e}")


# Основной класс приложения с интерфейсом
class IPApp(QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем основной layout
        self.setWindowTitle("Get IP Address")
        self.layout = QVBoxLayout()

        # Кнопка для получения IP
        self.button = QPushButton("Get IP")
        self.button.clicked.connect(self.start_fetching)
        self.layout.addWidget(self.button)

        # Метка для отображения результата
        self.label = QLabel("Your IP address will appear here")
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

        # Экземпляр QThread для асинхронного получения IP
        self.ip_fetcher = IPFetcher()
        self.ip_fetcher.finished.connect(self.display_ip)  # Подключаем сигнал к функции отображения

    def start_fetching(self):
        self.label.setText("Fetching IP address...")  # Обновляем текст метки
        self.ip_fetcher.start()  # Запускаем поток для получения IP

    def display_ip(self, ip):
        self.label.setText(f"Your IP address is: {ip}")  # Отображаем IP-адрес


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = IPApp()
    window.show()

    sys.exit(app.exec_())
