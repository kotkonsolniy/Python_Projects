import threading
import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel, QWidget
from PyQt5.QtCore import Qt

# Функция для нахождения суммы части массива
def partial_sum(arr, start, end, result, index):
    result[index] = sum(arr[start:end])

# Функция для нахождения суммы с использованием N потоков
def threaded_sum(arr, N):
    length = len(arr)
    result = [0] * N  # Массив для хранения промежуточных результатов
    threads = []
    part_size = length // N

    # Запуск N потоков
    for i in range(N):
        start = i * part_size
        # Последний поток берет все оставшиеся элементы
        end = (i + 1) * part_size if i != N - 1 else length
        thread = threading.Thread(target=partial_sum, args=(arr, start, end, result, i))
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    # Итоговая сумма
    return sum(result)


class SumApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Threaded Sum Application")
        self.setGeometry(100, 100, 400, 300)

        # Текстовое поле для ввода числа потоков
        self.thread_input_label = QLabel("Number of Threads:", self)
        self.thread_input = QLineEdit(self)
        self.thread_input.setPlaceholderText("Enter number of threads (e.g., 4, but no more than 10000)")

        # Кнопка для запуска вычислений
        self.start_button = QPushButton("Start Calculation", self)
        self.start_button.clicked.connect(self.start_calculation)

        # Текстовое поле для вывода результата
        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)

        # Layout для размещения виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.thread_input_label)
        layout.addWidget(self.thread_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.result_output)

        # Центральный виджет и установка layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_calculation(self):
        # Получаем количество потоков из текстового поля
        try:
            num_threads = int(self.thread_input.text())
            if num_threads <= 0:
                raise ValueError("Number of threads must be a positive integer.")
        except ValueError as e:
            self.result_output.setText(f"Invalid input: {str(e)}")
            return

        # Генерация массива для вычисления
        array = [i for i in range(1, 10000001)]  # Массив из 10 миллионов чисел

        # Запуск вычислений с замером времени
        start_time = time.time()
        total_sum = threaded_sum(array, num_threads)  # Нахождение суммы с N потоками
        elapsed_time = time.time() - start_time

        # Вывод результата в текстовое поле
        self.result_output.setText(f"Number of Threads: {num_threads}\n"
                                   f"Sum: {total_sum}\n"
                                   f"Time: {elapsed_time:.6f} seconds")


if __name__ == "__main__":
    # Запуск приложения
    app = QApplication(sys.argv)

    window = SumApp()
    window.show()

    sys.exit(app.exec_())
