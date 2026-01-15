# From: Zero to AI Agent, Chapter 5, Section 5.4
# File: exercise_1_5_4_solution.py

# Global constant
MINIMUM_BALANCE = 10

def create_account(name, initial_balance):
    """Create a new account dictionary"""
    if initial_balance < MINIMUM_BALANCE:
        print(f"Initial balance must be at least ${MINIMUM_BALANCE}")
        return None
    
    return {
        "name": name,
        "balance": initial_balance,
        "transactions": [f"Account opened with ${initial_balance}"]
    }

def deposit(account, amount):
    """Deposit money and return updated account"""
    if amount <= 0:
        print("Deposit amount must be positive")
        return account
    
    account["balance"] += amount
    account["transactions"].append(f"Deposited ${amount}")
    print(f"Deposited ${amount}. New balance: ${account['balance']}")
    return account

def withdraw(account, amount):
    """Withdraw money and return updated account"""
    if amount <= 0:
        print("Withdrawal amount must be positive")
        return account
    
    if account["balance"] - amount < MINIMUM_BALANCE:
        print(f"Insufficient funds! Must maintain minimum balance of ${MINIMUM_BALANCE}")
        return account
    
    account["balance"] -= amount
    account["transactions"].append(f"Withdrew ${amount}")
    print(f"Withdrew ${amount}. New balance: ${account['balance']}")
    return account

def get_balance(account):
    """Return current balance"""
    return account["balance"]

def print_statement(account):
    """Print account statement"""
    print(f"\n{'='*40}")
    print(f"Account Statement for {account['name']}")
    print(f"{'='*40}")
    print("Transaction History:")
    for transaction in account["transactions"]:
        print(f"  - {transaction}")
    print(f"{'='*40}")
    print(f"Current Balance: ${account['balance']}")
    print(f"{'='*40}\n")

# Test the system
account = create_account("Alice", 100)
if account:
    account = deposit(account, 50)
    account = withdraw(account, 30)
    account = withdraw(account, 115)  # Should fail
    
    balance = get_balance(account)
    print(f"\nAlice's balance: ${balance}")
    
    print_statement(account)