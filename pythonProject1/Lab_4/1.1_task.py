#тут представлена сереализация содержимого файла
import pickle #picle не поддерживает I/O

# Открываем файл и читаем его содержимое
with open("example.txt", "r") as file:
    content = file.read()

# Сериализуем содержимое файла в байты
serialized_content = pickle.dumps(content)

# Открываем файл для записи сериализованного содержимого
with open("serialized_file.pkl", "wb") as serialized_file:
    serialized_file.write(serialized_content)

# Выводим сериализованное содержимое в виде байтов
print(serialized_content)
print("Содержимое файла:", content)
