#сериализация встроенных функций невозможна, но можно сериализовать информацию
import pickle

data_to_print = "Hello, World!"
serialized_data = pickle.dumps(data_to_print)
deserialized_data = pickle.loads(serialized_data)

print(deserialized_data)