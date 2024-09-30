import urllib.request
import time
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget
from PyQt5.QtCore import Qt

# Список URL для загрузки
urls = [
    'https://www.yandex.ru', 'https://www.google.com',
    'https://habr.com', 'https://www.python.org',
    'https://isocpp.org',
]

# Функция для загрузки данных с одного URL
def read_url(url):
    with urllib.request.urlopen(url) as u:
        return u.read()

# Функция для потока, которая вызывает read_url и выводит длину содержимого
def fetch_url(url, output_widget):
    try:
        data = read_url(url)
        output_widget.append(f"Загружен {url}, размер: {len(data)} байт")
    except Exception as e:
        output_widget.append(f"Ошибка при загрузке {url}: {e}")

# Последовательная загрузка (один поток)
def sequential_download(output_widget):
    output_widget.append("Запуск последовательной загрузки...")
    start = time.time()

    # Последовательная загрузка всех URL
    for url in urls:
        read_url(url)

    elapsed_time = time.time() - start
    output_widget.append(f"Время работы (последовательно): {elapsed_time:.2f} секунд")

# Многопоточная загрузка (несколько потоков)
def threaded_download(output_widget):
    output_widget.append("Запуск многопоточной загрузки...")
    start = time.time()

    # Создаем список потоков
    threads = []
    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url, output_widget))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    elapsed_time = time.time() - start
    output_widget.append(f"Время работы (потоки): {elapsed_time:.2f} секунд")

# Основной класс интерфейса
class DownloadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("URL Downloader")
        self.setGeometry(100, 100, 600, 400)

        # Кнопка для последовательной загрузки
        self.sequential_button = QPushButton("Последовательная загрузка", self)
        self.sequential_button.clicked.connect(self.sequential)

        # Кнопка для многопоточной загрузки
        self.threaded_button = QPushButton("Многопоточная загрузка", self)
        self.threaded_button.clicked.connect(self.threaded)

        # Текстовое поле для вывода результатов
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        # Layout для размещения кнопок и текстового поля
        layout = QVBoxLayout()
        layout.addWidget(self.sequential_button)
        layout.addWidget(self.threaded_button)
        layout.addWidget(self.output)

        # Центральный виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Обработчик нажатия для последовательной загрузки
    def sequential(self):
        self.output.clear()
        sequential_download(self.output)

    # Обработчик нажатия для многопоточной загрузки
    def threaded(self):
        self.output.clear()
        threaded_download(self.output)

# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloadApp()
    window.show()
    sys.exit(app.exec_())
