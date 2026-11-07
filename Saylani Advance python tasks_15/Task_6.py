import itertools
from dataclasses import dataclass
from decimal import Decimal


class BankError(Exception):
    """Base class for all banking errors."""

class InvalidAmountError(BankError, ValueError):
    pass

class InsufficientFundsError(BankError):
    pass

class AccountNotFoundError(BankError):
    pass

class DuplicateAccountError(BankError):
    pass


@dataclass(frozen=True)
class Transaction:
    """Immutable record: assigning to any field raises FrozenInstanceError."""
    id: int
    action: str           
    amount: object         
    balance_after: object


_txn_ids = itertools.count(1)   


def _check_amount(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, Decimal)):
        raise TypeError("Amount must be an int or Decimal")
    if isinstance(amount, Decimal) and not amount.is_finite():
        raise InvalidAmountError("Amount must be finite")
    if amount <= 0:
        raise InvalidAmountError(f"Amount must be positive, got {amount}")


class Account:
    def __init__(self, account_id, opening_balance=0):
        if isinstance(opening_balance, bool) or not isinstance(opening_balance, (int, Decimal)):
            raise TypeError("Opening balance must be an int or Decimal")
        if opening_balance < 0:
            raise InvalidAmountError("Opening balance cannot be negative")
        self._id = account_id
        self._balance = opening_balance
        self._history = []
        if opening_balance > 0:
            self._record("open", opening_balance, next(_txn_ids))
    @property
    def account_id(self):
        return self._id

    @property
    def balance(self):
        return self._balance

    @property
    def history(self):
        return tuple(self._history)        
    def _record(self, action, amount, txn_id):
        self._history.append(Transaction(txn_id, action, amount, self._balance))

    def _credit(self, amount, action, txn_id):
        self._balance += amount
        self._record(action, amount, txn_id)

    def _debit(self, amount, action, txn_id):
        self._balance -= amount
        self._record(action, amount, txn_id)

    def _check_can_debit(self, amount):
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Account {self._id!r}: balance {self._balance} is less than {amount}"
            )
    def deposit(self, amount):
        _check_amount(amount)
        self._credit(amount, "deposit", next(_txn_ids))

    def withdraw(self, amount):
        _check_amount(amount)
        self._check_can_debit(amount)
        self._debit(amount, "withdraw", next(_txn_ids))

    def statement(self):
        return self.history

    def format_statement(self):
        lines = [f"Statement for {self._id}",
                 f"{'ID':>4}  {'Action':<13}{'Amount':>10}{'Balance':>10}"]
        lines += [f"{t.id:>4}  {t.action:<13}{t.amount:>10}{t.balance_after:>10}"
                  for t in self._history]
        return "\n".join(lines)


class Bank:
    def __init__(self):
        self._accounts = {}

    def open_account(self, account_id, opening_balance=0):
        if account_id in self._accounts:
            raise DuplicateAccountError(f"Account {account_id!r} already exists")
        account = Account(account_id, opening_balance)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id):
        try:
            return self._accounts[account_id]
        except KeyError:
            raise AccountNotFoundError(f"Account {account_id!r} does not exist") from None

    def deposit(self, account_id, amount):
        self.get_account(account_id).deposit(amount)

    def withdraw(self, account_id, amount):
        self.get_account(account_id).withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        _check_amount(amount)
        src = self.get_account(from_id)
        dst = self.get_account(to_id)
        if src is dst:
            raise BankError("Cannot transfer to the same account")
        src._check_can_debit(amount)

        txn_id = next(_txn_ids)             
        src._debit(amount, "transfer_out", txn_id)
        dst._credit(amount, "transfer_in", txn_id)

    def statement(self, account_id):
        return self.get_account(account_id).statement()