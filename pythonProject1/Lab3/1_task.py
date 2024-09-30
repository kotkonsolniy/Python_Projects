import asyncio
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal


class FactorialWorker(QThread):
    # Сигнал для отправки сообщений из потока в основной поток
    result_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    # Запуск асинхронного процесса в отдельном потоке
    async def factorial(self, name, number):
        f = 1
        for i in range(2, number + 1):
            self.result_signal.emit(f"Task {name}: Compute factorial({i})...\n")
            await asyncio.sleep(1)  # симуляция долгого вычисления
            f *= i
        self.result_signal.emit(f"Task {name}: factorial({number}) = {f}\n")

    async def run_factorials(self):
        await asyncio.gather(
            self.factorial("A", 2),
            self.factorial("B", 3),
            self.factorial("C", 4),
        )

    def run(self):
        asyncio.run(self.run_factorials())


class FactorialApp(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка интерфейса
        self.init_ui()

        # Создаем воркер для асинхронных вычислений
        self.worker = FactorialWorker()
        self.worker.result_signal.connect(self.update_output)

    def init_ui(self):
        self.setWindowTitle("Factorial Calculator")

        # Основной layout
        layout = QVBoxLayout()

        # Кнопка для запуска вычислений
        self.start_button = QPushButton("Start Factorial Calculation", self)
        self.start_button.clicked.connect(self.start_factorials)
        layout.addWidget(self.start_button)

        # Поле для вывода результатов
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def start_factorials(self):
        # Запускаем вычисления в отдельном потоке
        self.output_text.clear()  # Очищаем текстовое поле
        self.worker.start()

    def update_output(self, message):
        # Обновление текстового поля результатами
        self.output_text.append(message)


# Основной запуск приложения
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FactorialApp()
    window.show()
    sys.exit(app.exec_())
