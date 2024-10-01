import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


class InvalidNucleotideError(Exception):
    """Исключение, которое выбрасывается, если в строке содержатся недопустимые символы."""
    pass


class DNA:
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self._validate_sequence('ATGC')

    def _validate_sequence(self, allowed_bases):
        for base in self.sequence:
            if base not in allowed_bases:
                raise InvalidNucleotideError(f"Недопустимый нуклеотид '{base}' в последовательности ДНК.")

    def to_list(self):
        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        return [(base, complement[base]) for base in self.sequence]


class RNA:
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self._validate_sequence('AUGC')

    def _validate_sequence(self, allowed_bases):
        for base in self.sequence:
            if base not in allowed_bases:
                raise InvalidNucleotideError(f"Недопустимый нуклеотид '{base}' в последовательности РНК.")

    def to_list(self):
        return list(self.sequence)


class NucleotideHelper:
    @staticmethod
    def rna_to_dna(rna_sequence):
        rna_to_dna_map = {
            'A': 'T',
            'U': 'A',
            'G': 'C',
            'C': 'G'
        }
        dna_first_strand = ''.join(rna_to_dna_map[base] for base in rna_sequence)
        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        dna_second_strand = ''.join(complement[base] for base in dna_first_strand)
        return dna_first_strand, dna_second_strand

    @staticmethod
    def concatenate_rna(rna1, rna2):
        return rna1 + rna2

    @staticmethod
    def concatenate_dna(dna1, dna2):
        first_strand = dna1[0] + dna2[0]
        second_strand = dna1[1] + dna2[1]
        return [first_strand, second_strand]


class RNACrossOver:
    @staticmethod
    def crossover(rna1, rna2):
        result = []
        min_length = min(len(rna1), len(rna2))
        for i in range(min_length):
            result.append(random.choice([rna1[i], rna2[i]]))
        if len(rna1) > len(rna2):
            result.extend(rna1[min_length:])
        else:
            result.extend(rna2[min_length:])
        return ''.join(result)


class DNACrossOver:
    @staticmethod
    def crossover(dna1, dna2):
        first_strand1, second_strand1 = dna1
        first_strand2, second_strand2 = dna2

        crossed_first_strand = RNACrossOver.crossover(first_strand1, first_strand2)

        complement = {
            'A': 'T',
            'T': 'A',
            'G': 'C',
            'C': 'G'
        }
        crossed_second_strand = ''.join(complement[base] for base in crossed_first_strand)

        return [crossed_first_strand, crossed_second_strand]


class NucleotideComparator:
    @staticmethod
    def are_equal_dna_rna(dna, rna):
        rna_to_dna_map = {
            'A': 'T',
            'U': 'A',
            'G': 'C',
            'C': 'G'
        }
        rna_dna_sequence = ''.join(rna_to_dna_map[base] for base in rna)
        return dna[0] == rna_dna_sequence or dna[1] == rna_dna_sequence


# GUI класс
class NucleotideGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNA/RNA Operations")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout()

        # Поля ввода
        self.dna_input = QLineEdit(self)
        self.dna_input.setPlaceholderText("Введите последовательность ДНК (A, T, G, C)")
        layout.addWidget(self.dna_input)

        # Добавляем валидатор для ввода ДНК
        dna_validator = QRegExpValidator(QRegExp("[ATGC]*"))
        self.dna_input.setValidator(dna_validator)

        self.rna_input = QLineEdit(self)
        self.rna_input.setPlaceholderText("Введите последовательность РНК (A, U, G, C)")
        layout.addWidget(self.rna_input)

        # Добавляем валидатор для ввода РНК
        rna_validator = QRegExpValidator(QRegExp("[AUGC]*"))
        self.rna_input.setValidator(rna_validator)

        # Кнопки для выполнения операций
        self.concatenate_button = QPushButton("Склеить ДНК и РНК", self)
        self.concatenate_button.clicked.connect(self.concatenate_sequences)
        layout.addWidget(self.concatenate_button)

        self.crossover_button = QPushButton("Перемножить ДНК и РНК", self)
        self.crossover_button.clicked.connect(self.crossover_sequences)
        layout.addWidget(self.crossover_button)

        self.compare_button = QPushButton("Сравнить ДНК и РНК", self)
        self.compare_button.clicked.connect(self.compare_sequences)
        layout.addWidget(self.compare_button)

        # Поле для вывода результатов
        self.result_output = QTextEdit(self)
        layout.addWidget(self.result_output)

        self.setLayout(layout)

    def concatenate_sequences(self):
        dna_seq = self.dna_input.text()
        rna_seq = self.rna_input.text()

        try:
            dna = DNA(dna_seq)
            rna = RNA(rna_seq)
            concatenated_dna = NucleotideHelper.concatenate_dna([dna.sequence, dna.sequence], [dna.sequence, dna.sequence])
            concatenated_rna = NucleotideHelper.concatenate_rna(rna.sequence, rna.sequence)
            self.result_output.setText(f"Склеенная ДНК: {concatenated_dna}\nСклеенная РНК: {concatenated_rna}")
        except InvalidNucleotideError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def crossover_sequences(self):
        dna_seq = self.dna_input.text()
        rna_seq = self.rna_input.text()

        try:
            dna = DNA(dna_seq)
            rna = RNA(rna_seq)
            crossed_dna = DNACrossOver.crossover([dna.sequence, dna.sequence], [dna.sequence, dna.sequence])
            crossed_rna = RNACrossOver.crossover(rna.sequence, rna.sequence)
            self.result_output.setText(f"Перемноженная ДНК: {crossed_dna}\nПеремноженная РНК: {crossed_rna}")
        except InvalidNucleotideError as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def compare_sequences(self):
        dna_seq = self.dna_input.text()
        rna_seq = self.rna_input.text()

        try:
            dna = DNA(dna_seq)
            rna = RNA(rna_seq)
            are_equal = NucleotideComparator.are_equal_dna_rna([dna.sequence, dna.sequence], rna.sequence)
            result_text = "Равны" if are_equal else "Не равны"
            self.result_output.setText(f"Сравнение ДНК и РНК: {result_text}")
        except InvalidNucleotideError as e:
            QMessageBox.warning(self, "Ошибка", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = NucleotideGUI()
    gui.show()
    sys.exit(app.exec_())
