import random


class InvalidSequenceError(Exception):
    """Ошибка, вызываемая при недопустимых символах в последовательности."""
    pass


class RNA:
    valid_bases = "AUGC"

    def init(self, sequence):
        # Проверка на допустимые символы
        if any(base not in self.valid_bases for base in sequence):
            raise InvalidSequenceError("Недопустимые символы в РНК последовательности")
        self.sequence = sequence

    def getitem(self, index):
        return self.sequence[index]

    def len(self):
        return len(self.sequence)

    def repr(self):
        return f"RNA({self.sequence})"

    def str(self):
        return self.sequence

    def to_dna(self):
        complement_map = {"A": "T", "U": "A", "G": "C", "C": "G"}
        first_strand = ''.join(complement_map[base] for base in self.sequence)
        second_strand = ''.join(complement_map[base] for base in first_strand)
        return DNA(first_strand, second_strand)

    def add(self, other):
        if isinstance(other, RNA):
            return RNA(self.sequence + other.sequence)
        raise TypeError("Можно складывать только с другой РНК")

    def mul(self, other):
        if not isinstance(other, RNA):
            raise TypeError("Можно перемножать только с другой РНК")

        max_len = max(len(self), len(other))
        result = []
        for i in range(max_len):
            base1 = self.sequence[i % len(self)]
            base2 = other.sequence[i % len(other)]
            result.append(random.choice([base1, base2]))
        return RNA(''.join(result))

    def eq(self, other):
        return isinstance(other, RNA) and self.sequence == other.sequence


class DNA:
    valid_bases = "ATGC"

    def init(self, first_strand, second_strand=None):
        if any(base not in self.valid_bases for base in first_strand):
            raise InvalidSequenceError("Недопустимые символы в ДНК последовательности")

        # Если вторая цепочка не дана, строим комплиментарную автоматически
        if second_strand is None:
            complement_map = {"A": "T", "T": "A", "G": "C", "C": "G"}
            second_strand = ''.join(complement_map[base] for base in first_strand)

        # Проверка на соответствие второй цепочки первой
        if len(first_strand) != len(second_strand):
            raise ValueError("Длины цепочек ДНК не совпадают")

        self.first_strand = first_strand
        self.second_strand = second_strand

    def getitem(self, index):
        return (self.first_strand[index], self.second_strand[index])

    def len(self):
        return len(self.first_strand)

    def repr(self):
        return f"DNA({self.first_strand}, {self.second_strand})"

    def str(self):
        return f"{self.first_strand}\n{self.second_strand}"

    def add(self, other):
        if isinstance(other, DNA):
            return DNA(self.first_strand + other.first_strand, self.second_strand + other.second_strand)
        raise TypeError("Можно складывать только с другой ДНК")

    def mul(self, other):
        if not isinstance(other, DNA):
            raise TypeError("Можно перемножать только с другой ДНК")

        max_len = max(len(self.first_strand), len(other.first_strand))
        result_first_strand = []

        for i in range(max_len):
            base1 = self.first_strand[i % len(self.first_strand)]
            base2 = other.first_strand[i % len(other.first_strand)]
            result_first_strand.append(random.choice([base1, base2]))

        result_first_strand = ''.join(result_first_strand)
        complement_map = {"A": "T", "T": "A", "G": "C", "C": "G"}
        result_second_strand = ''.join(complement_map[base] for base in result_first_strand)

        return DNA(result_first_strand, result_second_strand)

    def eq(self, other):
        return isinstance(other, DNA) and self.first_strand == other.first_strand and self.second_strand == other.second_strand