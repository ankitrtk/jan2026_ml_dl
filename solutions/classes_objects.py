import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = (x**2 + y**2) ** 0.5
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)




obj1 = Vector(1/2**.5, 1/2**.5)
obj2 = Vector(1/2**.5, 1/2**.5)
print(obj1.x, obj1.y, obj1.h)