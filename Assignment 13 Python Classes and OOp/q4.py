### Q4. Vehicle Rental System | Intermediate
### Create a base class Vehicle with brand, model, and daily rental rate. Implement calculate_rent(days). Derive Car, which adds a fixed insurance fee of Rs. 1,000 per rental, and Bike, which applies a 10% discount to the base rental amount. Override calculate_rent() and reuse the parent implementation with super(). Reject rental durations of zero or fewer days. Test both vehicle types for a three-day rental.

class Vehicle:

    def __init__(self, brand: str, model: str, rate: float):
        self.brand = brand
        self.model = model
        self.rate = rate

    def calculate_rent(self, days: int) -> float:
        return self.rate * days


class Car(Vehicle):

    def calculate_rent(self, days: int) -> float | str:
        if days <= 0:
            return "Invalid days"
        base_rent = super().calculate_rent(days)
        return base_rent + 1000  # Fixed insurance fee


class Bike(Vehicle):

    def calculate_rent(self, days: int) -> float | str:
        if days <= 0:
            return "Invalid days"
        base_rent = super().calculate_rent(days)
        return base_rent - (base_rent * 0.10)  # 10% discount


if __name__ == "__main__":
    car = Car("Toyota", "Corolla", 5000)
    bike = Bike("Yamaha", "YBR", 2000)

    print(f"Car rent for 3 days: {car.calculate_rent(3)}")
    print(f"Bike rent for 3 days: {bike.calculate_rent(3)}")