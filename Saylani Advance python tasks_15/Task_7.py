from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def _money(value, field):
    """Validate a non-negative number and convert it to Decimal.
    str() avoids binary float noise, so 0.10 becomes exactly Decimal('0.10')."""
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise TypeError(f"{field} must be a number")
    d = Decimal(str(value))
    if not d.is_finite() or d < 0:
        raise ValueError(f"{field} must be a finite, non-negative number")
    return d


class Employee(ABC):
    """Abstract base: Employee() raises TypeError because calculate_pay is abstract."""

    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def calculate_pay(self):
        """Return this employee's pay for one pay period as a Decimal."""

    def __repr__(self):
        return f"{type(self).__name__}({self._name!r})"


class SalariedEmployee(Employee):
    def __init__(self, name, salary):
        super().__init__(name)
        self._salary = _money(salary, "salary")      

    def calculate_pay(self):
        return self._salary.quantize(CENT, ROUND_HALF_UP)


class HourlyEmployee(Employee):
    REGULAR_HOURS = Decimal("40")
    OVERTIME_MULTIPLIER = Decimal("1.5")

    def __init__(self, name, rate, hours):
        super().__init__(name)
        self._rate = _money(rate, "rate")
        self._hours = _money(hours, "hours")

    def calculate_pay(self):
        regular = min(self._hours, self.REGULAR_HOURS)
        overtime = max(self._hours - self.REGULAR_HOURS, Decimal(0))
        pay = self._rate * regular + self._rate * self.OVERTIME_MULTIPLIER * overtime
        return pay.quantize(CENT, ROUND_HALF_UP)


class CommissionEmployee(Employee):
    def __init__(self, name, base, sales, rate):
        super().__init__(name)
        self._base = _money(base, "base")
        self._sales = _money(sales, "sales")
        self._rate = _money(rate, "rate")

    def calculate_pay(self):
        return (self._base + self._sales * self._rate).quantize(CENT, ROUND_HALF_UP)


def payroll_summary(employees):
    """Works for any Employee subclass with no type checks (polymorphism)."""
    lines = [(e.name, type(e).__name__, e.calculate_pay()) for e in employees]
    return {"lines": lines, "total": sum((pay for _, _, pay in lines), Decimal("0.00"))}


def format_payroll(employees):
    summary = payroll_summary(employees)
    out = [f"{'Name':<10}{'Type':<20}{'Pay':>10}"]
    out += [f"{n:<10}{k:<20}{p:>10.2f}" for n, k, p in summary["lines"]]
    out.append(f"{'Total':<30}{summary['total']:>10.2f}")
    return "\n".join(out)