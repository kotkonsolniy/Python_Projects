#сериализация класса, но pickle может сериализовать не все встроенные клласы и функции, сериализовать обекты проще
import pickle
from collections import deque

serialized_deque_class = pickle.dumps(deque)
deserialized_deque_class = pickle.loads(serialized_deque_class)
my_deque = deserialized_deque_class([1, 2, 3])
print(my_deque)