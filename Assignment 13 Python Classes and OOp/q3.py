### Q3. Employee Roles | Beginner
### Create a parent class Employee that stores a name and employee ID and provides display_details(). Derive Developer (programming language) and Manager (team size). Use super() to initialize inherited attributes. Override display_details() in each child class to include both shared and role-specific information. Create and test one object of each type.
### ```[cite: 11]

class Employee:

    def __init__(self, name: str, emp_id: str):
        self.name = name
        self.emp_id = emp_id

    def display_details(self) -> None:
        print(f"ID: {self.emp_id}, Name: {self.name}")


class Developer(Employee):

    def __init__(self, name: str, emp_id: str, lang: str):
        super().__init__(name, emp_id)
        self.lang = lang

    def display_details(self) -> None:
        print(f"Developer - ID: {self.emp_id}, Name: {self.name}, Language: {self.lang}")


class Manager(Employee):

    def __init__(self, name: str, emp_id: str, team_size: int):
        super().__init__(name, emp_id)
        self.team_size = team_size

    def display_details(self) -> None:
        print(f"Manager - ID: {self.emp_id}, Name: {self.name}, Team Size: {self.team_size}")


if __name__ == "__main__":
    emp = Employee("Ahmed", "E01")
    dev = Developer("Ali", "E02", "Python")
    mgr = Manager("Sara", "E03", 5)

    emp.display_details()
    dev.display_details()
    mgr.display_details()