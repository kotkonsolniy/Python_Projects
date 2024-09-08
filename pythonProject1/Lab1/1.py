width = float(input("Введите ширину: "))
height = float(input("Введите высоту: "))
class Shape:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Triangle(Shape):
    def area(self):
        return 0.5 * self.width * self.height
class Rectangle(Shape):
    def area(self):
        return self.width * self.height
triangle = Triangle(width, height)
print("Площадь треугольника:", triangle.area())
rectangle = Rectangle(width, height)
print("Площадь четырехугольника:", rectangle.area())