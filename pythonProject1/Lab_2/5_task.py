import random

# Исключение для некорректных последовательностей
class InvalidSequenceError(Exception):
    pass

# Класс для работы с РНК
class RNA:
    valid_bases = {'A', 'U', 'G', 'C'}

    def __init__(self, sequence):
        if not set(sequence).issubset(self.valid_bases):
            raise InvalidSequenceError(f"Недопустимые символы в последовательности РНК: {sequence}")
        self.sequence = sequence

    def __getitem__(self, index):
        return self.sequence[index]

    def __add__(self, other):
        if isinstance(other, RNA):
            return RNA(self.sequence + other.sequence)
        raise TypeError("Можно складывать только с другим объектом RNA")

    def __mul__(self, other):
        if isinstance(other, RNA):
            min_length = min(len(self.sequence), len(other.sequence))
            combined_seq = ''.join(random.choice([self.sequence[i], other.sequence[i]]) for i in range(min_length))
            combined_seq += self.sequence[min_length:] + other.sequence[min_length:]
            return RNA(combined_seq)
        raise TypeError("Можно перемножать только с другим объектом RNA")

    def to_dna(self):
        dna_first_strand = self.sequence.replace('A', 'T').replace('U', 'A').replace('G', 'C').replace('C', 'G')
        return DNA(dna_first_strand, DNA.complementary_strand(dna_first_strand))

    def __eq__(self, other):
        return isinstance(other, RNA) and self.sequence == other.sequence

    def __repr__(self):
        return f"RNA('{self.sequence}')"

    def __str__(self):
        return self.sequence


# Класс для работы с ДНК
class DNA:
    valid_bases = {'A', 'T', 'G', 'C'}

    def __init__(self, first_strand, second_strand=None):
        if not set(first_strand).issubset(self.valid_bases):
            raise InvalidSequenceError(f"Недопустимые символы в первой цепи ДНК: {first_strand}")
        if second_strand is None:
            second_strand = self.complementary_strand(first_strand)
        if len(first_strand) != len(second_strand) or not set(second_strand).issubset(self.valid_bases):
            raise InvalidSequenceError("Цепочки ДНК должны быть одинаковой длины и содержать только допустимые основания.")
        self.first_strand = first_strand
        self.second_strand = second_strand

    @staticmethod
    def complementary_strand(strand):
        return strand.replace('A', 'T').replace('T', 'A').replace('G', 'C').replace('C', 'G')

    def __getitem__(self, index):
        return self.first_strand[index], self.second_strand[index]

    def __add__(self, other):
        if isinstance(other, DNA):
            return DNA(self.first_strand + other.first_strand, self.second_strand + other.second_strand)
        raise TypeError("Можно складывать только с другим объектом DNA")

    def __mul__(self, other):
        if isinstance(other, DNA):
            min_length = min(len(self.first_strand), len(other.first_strand))
            combined_first_strand = ''.join(random.choice([self.first_strand[i], other.first_strand[i]]) for i in range(min_length))
            combined_first_strand += self.first_strand[min_length:] + other.first_strand[min_length:]
            combined_second_strand = self.complementary_strand(combined_first_strand)
            return DNA(combined_first_strand, combined_second_strand)
        raise TypeError("Можно перемножать только с другим объектом DNA")

    def __eq__(self, other):
        return isinstance(other, DNA) and self.first_strand == other.first_strand and self.second_strand == other.second_strand

    def __repr__(self):
        return f"DNA('{self.first_strand}', '{self.second_strand}')"

    def __str__(self):
        return f"Первая цепь: {self.first_strand}\nВторая цепь: {self.second_strand}"


# Пример использования:

# Создаем объекты РНК
rna1 = RNA("AUGC")
rna2 = RNA("CGGA")

# Индексация
print(rna1[0])  # A
print(rna2[2])  # G

# Склеивание РНК
rna3 = rna1 + rna2
print(rna3)  # AUGCCGGA

# Перемножение РНК
rna4 = rna1 * rna2
print(rna4)  # Случайная последовательность, например: AGGC или CGGA

# Конвертация РНК в ДНК
dna1 = rna1.to_dna()
print(dna1)  # Первая цепь: TACC Вторая цепь: ATGG

# Создаем объекты ДНК
dna2 = DNA("ATGC", "TACG")
dna3 = DNA("GGCC", "CCGG")

# Индексация ДНК
print(dna2[0])  # ('A', 'T')
print(dna3[1])  # ('G', 'C')

# Склеивание ДНК
dna4 = dna2 + dna3
print(dna4)  # Первая цепь: ATGCGGCC Вторая цепь: TACGCCGG

# Перемножение ДНК
dna5 = dna2 * dna3
print(dna5)  # Случайная последовательность

# Проверка на равенство
print(rna1 == rna2)  # False
print(dna2 == DNA("ATGC", "TACG"))  # True
