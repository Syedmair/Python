### Q8. Payment Gateway | Intermediate
### Define an abstract PaymentMethod class with abstract methods pay(amount) and refund(amount). Implement CardPayment, WalletPayment, and BankTransferPayment. Each method must display the payment method, transaction type, and amount. Validate that transaction amounts are positive. Write process_transaction(method, amount) to call pay() for any supported payment method. Extension: Add a new payment method without changing process_transaction().
### ```[cite: 14]

from abc import ABC, abstractmethod


class PaymentMethod(ABC):

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CardPayment(PaymentMethod):

    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using Credit/Debit Card.")


class WalletPayment(PaymentMethod):

    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using Digital Wallet.")


class BankTransferPayment(PaymentMethod):

    def pay(self, amount: float) -> None:
        print(f"Paid {amount} using Bank Transfer.")


def process_transaction(method: PaymentMethod, amount: float) -> None:
    if amount <= 0:
        print("Amount must be positive!")
        return
    method.pay(amount)


if __name__ == "__main__":
    process_transaction(CardPayment(), 5000)
    process_transaction(WalletPayment(), 1500)
    process_transaction(BankTransferPayment(), 12000)