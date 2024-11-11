import numpy as np

vector_1 = np.arange(12,43)
print("Вектор с числами от 12 до 42: \n", vector_1)

vector_2 = np.zeros(12)
vector_2[4] = 1
print("Вектор из 12 нулей и 1 на 5ом месте: \n", vector_2)

matrix = np.arange(9).reshape(3, 3)
print("Матрица 3на3 с числами от 0 до 9: \n", matrix)

plus_numbers = np.array([1, 2, 0, 0, 4, 0])[np.array([1, 2, 0, 0, 4, 0]) > 0]
print("Положительные элементы заданного массива: \n", plus_numbers)

matrix1_5 = np.random.rand(5, 3)
matrix2_5 = np.random.rand(3, 2)
proiz = np.dot(matrix1_5, matrix2_5)
print("Произведение матриц равно: \n", proiz)

matrix_6 = np.ones((10, 10))
matrix_6[0, :] = 0
matrix_6[-1, :] = 0
matrix_6[:, 0] = 0
matrix_6[:, -1] = 0
print("Mатрица с 1, окантованная 0: \n", matrix_6)

random_vector = np.random.rand(10)
sort_vector = np.sort(random_vector)
print(" Рандомный вектор: \n", random_vector, "\n", "Отсортированный вектор: \n", sort_vector)

print("Эквивалент функции enumerate для numpy массивов: np.ndenumerate")


random_matrix = np.random.rand(5, 3)
normalized_matrix = (random_matrix - np.mean(random_matrix, axis=0)) / np.std(random_matrix, axis=0)
print("Рандомный вектор и его нормализованная версия:")
print("Исходная матрица:")
print(random_matrix)
print("Нормализованная матрица:")
print(normalized_matrix)

given_number = 3.5
vector_10 = np.array([1, 2, 3, 4, 5])
closest_element = vector_10[np.argmin(np.abs(vector_10 - given_number))]
print("Ближайший элемент к числу 3.5 в векторе [1, 2, 3, 4, 5]:")
print(closest_element)

N = 3
vector_11 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
largest_values = np.partition(vector_11, -N)[-N:]
print("Три наибольших значения в векторе [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:")
print(largest_values)