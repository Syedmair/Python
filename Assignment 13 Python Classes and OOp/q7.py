### Q7. Shape Calculator | Beginner
### Use ABC and @abstractmethod to define an abstract Shape class with area() and perimeter(). Implement both methods in Circle and Rectangle. Accept dimensions through constructors and use pi = 3.14159. Test a circle with radius 5 and a rectangle with width 4 and height 6. Attempt to instantiate Shape directly and explain the outcome.
### ```[cite: 13, 14]

from abc import ABC, abstractmethod


class Shape(ABC):

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


class Circle(Shape):

    def __init__(self, radius: float):
        self.radius = radius
        self.pi = 3.14159

    def area(self) -> float:
        return self.pi * (self.radius ** 2)

    def perimeter(self) -> float:
        return 2 * self.pi * self.radius


class Rectangle(Shape):

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


if __name__ == "__main__":
    c = Circle(5)
    r = Rectangle(4, 6)

    print(f"Circle -> Area: {c.area():.2f}, Perimeter: {c.perimeter():.2f}")
    print(f"Rectangle -> Area: {r.area()}, Perimeter: {r.perimeter()}")