### Q6. Checkout Discount Calculator | Intermediate
### Create RegularCustomer, PremiumCustomer, and VIPCustomer classes, each implementing final_price(amount). Apply discounts of 5%, 10%, and 20%, respectively. Write print_receipt(customer, amount) so that it works with any customer type. For a bill of Rs. 10,000, show the final amount for each type. Reject negative bill amounts. Extension: Add GoldCustomer with a 15% discount without modifying print_receipt().
### ```[cite: 13]

class RegularCustomer:

    def final_price(self, amount: float) -> float:
        return amount - (amount * 0.05)


class PremiumCustomer:

    def final_price(self, amount: float) -> float:
        return amount - (amount * 0.10)


class VIPCustomer:

    def final_price(self, amount: float) -> float:
        return amount - (amount * 0.20)


def print_receipt(customer, amount: float) -> None:
    if amount < 0:
        print("Invalid amount!")
        return
    final = customer.final_price(amount)
    print(f"Customer Type: {type(customer).__name__} | Bill: {amount} | Final: {final}")


if __name__ == "__main__":
    bill = 10000
    print_receipt(RegularCustomer(), bill)
    print_receipt(PremiumCustomer(), bill)
    print_receipt(VIPCustomer(), bill)