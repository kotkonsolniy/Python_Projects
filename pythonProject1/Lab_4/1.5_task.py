#может быть сложной, так как функции могут иметь зависимости, которые не могут быть сериализованы
import pickle

class MyClass:
    def __init__(self, value):
        self.value = value

    def double(self):
        return self.value * 2

my_object = MyClass(5)
serialized_object = pickle.dumps(my_object)
deserialized_object = pickle.loads(serialized_object)

#использование десериализованного объекта
result = deserialized_object.double()
print(result)  # Вывод: 10