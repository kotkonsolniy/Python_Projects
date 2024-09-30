import multiprocessing
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox


# Функция для процесса
def worker(lst):
    lst.append('sos_help')


# Функция для запуска процессов
def run_processes(output_widget):
    manager = multiprocessing.Manager()
    LIST = manager.list()

    # Создаем и запускаем процессы
    processes = [
        multiprocessing.Process(target=worker, args=(LIST,))
        for _ in range(5)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    result = " ".join(LIST)
    # Отображаем результат в сообщении
    QMessageBox.information(output_widget, "Результат", f"Список после выполнения процессов: {result}")


# Основной класс интерфейса
class ProcessApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Многопроцессорное приложение")
        self.setGeometry(100, 100, 400, 200)

        # Кнопка для запуска процессов
        self.start_button = QPushButton("Запустить процессы", self)
        self.start_button.clicked.connect(self.run_processes)

        # Layout для размещения кнопки
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)

        # Центральный виджет
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Обработчик нажатия кнопки
    def run_processes(self):
        run_processes(self)


if __name__ == "__main__":
    # Запуск приложения
    multiprocessing.freeze_support()  # Нужно для Windows при запуске многопроцессорности
    app = QApplication(sys.argv)
    window = ProcessApp()
    window.show()
    sys.exit(app.exec_())
