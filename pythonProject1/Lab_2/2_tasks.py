import math


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_string(cls, s):
        try:
            x, y, z = map(float, s.split(','))
            return cls(x, y, z)
        except ValueError:
            raise ValueError("Неверный формат строки. Ожидается формат 'x,y,z'.")

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __eq__(self, other):
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __ne__(self, other):
        return not self.__eq__(other)


def cross_product(v1, v2):
    return Vector(
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


def scalar_triple_product(v1, v2, v3):
    cross_prod = cross_product(v2, v3)
    return v1 * cross_prod


def distance(v1, v2):
    return math.sqrt((v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2)


def perimeter(v1, v2, v3):
    return (distance(v1, v2) + distance(v2, v3) + distance(v3, v1))


def triangle_area(v1, v2, v3):
    a = v2 - v1
    b = v3 - v1
    cross_prod = cross_product(a, b)
    return 0.5 * cross_prod.length()


def farthest_point(points):
    max_length = 0
    farthest = None
    for point in points:
        if point.length() > max_length:
            max_length = point.length()
            farthest = point
    return farthest


def center_of_mass(points):
    if not points:
        return None
    n = len(points)
    sum_x = sum(point.x for point in points)
    sum_y = sum(point.y for point in points)
    sum_z = sum(point.z for point in points)
    return Vector(sum_x / n, sum_y / n, sum_z / n)


def parallelogram_area(v1, v2):
    cross_prod = cross_product(v1, v2)
    return cross_prod.length()


def parallelepiped_volume(v1, v2, v3):
    return abs(scalar_triple_product(v1, v2, v3))


def max_perimeter(points):
    max_perim = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                perim = perimeter(points[i], points[j], points[k])
                if perim > max_perim:
                    max_perim = perim
    return max_perim


def max_area(points):
    max_area = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                area = triangle_area(points[i], points[j], points[k])
                if area > max_area:
                    max_area = area
    return max_area


if __name__ == "__main__":
    try:
        n = int(input("Введите количество точек: "))
        points = []
        for _ in range(n):
            point_input = input("Введите координаты точки в формате 'x,y,z': ")
            points.append(Vector.from_string(point_input))

        print(f"Точка, наиболее удаленная от начала координат: {farthest_point(points)}")
        print(f"Центр масс: {center_of_mass(points)}")

        if n >= 2:
            v1 = Vector.from_string(input("Введите первый вектор в формате 'x,y,z': "))
            v2 = Vector.from_string(input("Введите второй вектор в формате 'x,y,z': "))
            print(f"Площадь параллелограмма: {parallelogram_area(v1, v2)}")

        if n >= 3:
            v1 = Vector.from_string(input("Введите первый вектор для параллелепипеда в формате 'x,y,z': "))
            v2 = Vector.from_string(input("Введите второй вектор для параллелепипеда в формате 'x,y,z': "))
            v3 = Vector.from_string(input("Введите третий вектор для параллелепипеда в формате 'x,y,z': "))
            print(f"Объём параллелепипеда: {parallelepiped_volume(v1, v2, v3)}")

        if n >= 3:
            print(f"Максимальный периметр треугольника: {max_perimeter(points)}")
            print(f"Максимальная площадь треугольника: {max_area(points)}")

    except ValueError as e:
        print(f"Ошибка: {e}")
