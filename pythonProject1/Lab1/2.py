class Mother:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return  f"{self.__name}"

class Daughter(Mother):
    def __init__(self, name, age):
        super().__init__(name)
        self.__age = age

    def __str__(self):
        return f"Daughter's name is {self._Mother__name} and she is {self.__age} years old"

# Пример использования
mother = Mother("Jana")
daughter = Daughter("Alisa", 10)

print("Mother's name is", mother)
print(daughter)