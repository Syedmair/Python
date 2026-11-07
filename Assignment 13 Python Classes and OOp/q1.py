### Q1. Student Result Manager | Beginner
### Create a Student class with a public name, protected _marks, and private __grade attributes. Initialize the student through a constructor. Implement set_marks(marks), which accepts only values from 0 to 100, along with get_marks() and get_grade(). Assign grade A for 80 to 100, B for 60 to 79, C for 40 to 59, and F below 40. Demonstrate both a valid and an invalid marks update. Extension: Attempt direct access to __grade and explain the result.
###```[cite: 10, 11]


class Student:

    def __init__(self, name: str, marks: int = 0):
        self.name = name
        self._marks = 0
        self.__grade = "F"
        self.set_marks(marks)

    def set_marks(self, marks: int) -> None:
        if 0 <= marks <= 100:
            self._marks = marks
            self.__calculate_grade()
        else:
            print("Invalid marks! Must be between 0 and 100.")

    def __calculate_grade(self) -> None:
        if self._marks >= 80:
            self.__grade = "A"
        elif self._marks >= 60:
            self.__grade = "B"
        elif self._marks >= 40:
            self.__grade = "C"
        else:
            self.__grade = "F"

    def get_marks(self) -> int:
        return self._marks

    def get_grade(self) -> str:
        return self.__grade


if __name__ == "__main__":
    student = Student("Ali", 85)
    print(f"Name: {student.name}, Marks: {student.get_marks()}, Grade: {student.get_grade()}")

    student.set_marks(105)
    student.set_marks(55)
    print(f"Updated Marks: {student.get_marks()}, Grade: {student.get_grade()}")