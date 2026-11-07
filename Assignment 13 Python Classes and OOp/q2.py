### Q2. Secure Bank Account | Intermediate
### Create a BankAccount class with a public account holder name, private __balance, and private __pin. Implement deposit(amount), withdraw(amount, pin), and get_balance(pin). Reject zero or negative deposits, withdrawals exceeding the available balance, and incorrect PINs. Demonstrate a successful deposit, a successful withdrawal, and two rejected operations. Extension: Explain why double underscores do not provide true security.
### ```[cite: 11]

class BankAccount:

    def __init__(self, holder_name: str, balance: float, pin: int):
        self.holder_name = holder_name
        self.__balance = balance
        self.__pin = pin

    def deposit(self, amount: float) -> None:
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}. New Balance: {self.__balance}")
        else:
            print("Invalid deposit amount!")

    def withdraw(self, amount: float, pin: int) -> None:
        if pin != self.__pin:
            print("Wrong PIN!")
        elif amount <= 0:
            print("Invalid withdrawal amount!")
        elif amount > self.__balance:
            print("Insufficient balance!")
        else:
            self.__balance -= amount
            print(f"Withdrawn: {amount}. Remaining Balance: {self.__balance}")

    def get_balance(self, pin: int) -> float | None:
        if pin == self.__pin:
            return self.__balance
        print("Wrong PIN!")
        return None


if __name__ == "__main__":
    account = BankAccount("Zeeshan", 10000, 1234)
    account.deposit(2000)
    account.withdraw(3000, 1234)
    account.withdraw(5000, 9999)
    print(f"Final Balance: {account.get_balance(1234)}")