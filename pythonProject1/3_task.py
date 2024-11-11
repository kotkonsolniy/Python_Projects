import numpy as np
import timeit
import pandas as pd
import psutil
import multiprocessing


x = np.random.random(size=10**6)
y = np.random.random(size=10**6)


def elementwise_operations_loop(x, y):
    sum_result = np.zeros_like(x)
    diff_result = np.zeros_like(x)
    prod_result = np.zeros_like(x)
    div_result = np.zeros_like(x)
    for i in range(len(x)):
        sum_result[i] = x[i] + y[i]
        diff_result[i] = x[i] - y[i]
        prod_result[i] = x[i] * y[i]
        div_result[i] = x[i] / y[i]
    return sum_result, diff_result, prod_result, div_result


sum_result = x + y
diff_result = x - y
prod_result = x * y
div_result = x / y


loop_time = timeit.timeit('elementwise_operations_loop(x, y)', globals=globals(), number=10)
print(f"Время выполнения с циклом: {loop_time} сек")

numpy_time = timeit.timeit('x + y', globals=globals(), number=10)
print(f"Время выполнения с оператором +: {numpy_time} сек")

numpy_time = timeit.timeit('x - y', globals=globals(), number=10)
print(f"Время выполнения с оператором -: {numpy_time} сек")

numpy_time = timeit.timeit('x * y', globals=globals(), number=10)
print(f"Время выполнения с оператором *: {numpy_time} сек")

numpy_time = timeit.timeit('x / y', globals=globals(), number=10)
print(f"Время выполнения с оператором /: {numpy_time} сек")


def check_cpu_usage():
    cpu_count = multiprocessing.cpu_count()
    print(f"Количество ядер процессора: {cpu_count}")
    print("Уровень загрузки ядер процессора:")
    for i in range(cpu_count):
        print(f"Ядро {i}: {psutil.cpu_percent(interval=1, percpu=True)[i]}%")


dot_time = timeit.timeit('np.dot(x, y)', globals=globals(), number=10)
print(f"Время выполнения np.dot: {dot_time} сек")
check_cpu_usage()


min_time = timeit.timeit('np.min(x)', globals=globals(), number=10)
print(f"Время выполнения np.min: {min_time} сек")

max_time = timeit.timeit('np.max(x)', globals=globals(), number=10)
print(f"Время выполнения np.max: {max_time} сек")

builtin_min_time = timeit.timeit('min(x)', globals=globals(), number=10)
print(f"Время выполнения встроенной функции min: {builtin_min_time} сек")

builtin_max_time = timeit.timeit('max(x)', globals=globals(), number=10)
print(f"Время выполнения встроенной функции max: {builtin_max_time} сек")


mean_x = np.mean(x)
mean_y = np.mean(y)
var_x = np.var(x)
var_y = np.var(y)
print(f"Математическое ожидание x: {mean_x}, y: {mean_y}")
print(f"Дисперсия x: {var_x}, y: {var_y}")


less_than_0 = np.sum(x < 0)
greater_than_1 = np.sum(x > 1)
greater_than_1_5 = np.sum(x > 1.5)
print(f"Элементов меньше 0: {less_than_0}, больше 1: {greater_than_1}, больше 1.5: {greater_than_1_5}")


elements_in_segment = y[(y >= 0) & (y <= 0.5)]
print(f"Элементы из отрезка [0, 1/2]: {elements_in_segment}")


data = np.column_stack((x, y))
df = pd.DataFrame(data, columns=['x', 'y'])
df.to_csv('output.csv', index=False)
print("Массивы x и y сохранены в файл output.csv")