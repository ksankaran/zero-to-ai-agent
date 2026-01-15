# From: Zero to AI Agent, Chapter 5, Section 5.8
# understanding_self.py - How 'self' works in classes

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner      # THIS account's owner
        self.balance = balance  # THIS account's balance

    def deposit(self, amount):
        self.balance += amount  # Add to THIS account's balance
        return f"Deposited ${amount}. New balance: ${self.balance}"

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        return f"Withdrew ${amount}. New balance: ${self.balance}"


# Two different accounts, each with their own data
alice_account = BankAccount("Alice", 1000)
bob_account = BankAccount("Bob", 500)

print(alice_account.deposit(200))   # Alice's balance: 1200
print(bob_account.withdraw(100))    # Bob's balance: 400

# They don't affect each other!
print(f"Alice: ${alice_account.balance}")  # 1200
print(f"Bob: ${bob_account.balance}")      # 400
