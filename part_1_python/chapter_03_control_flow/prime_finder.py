# From: Zero to AI Agent, Chapter 3, Section 3.6
# prime_finder.py

print("🔢 Prime Number Finder\n")

limit = int(input("Find primes up to: "))
print(f"\nPrime numbers from 2 to {limit}:")

for num in range(2, limit + 1):
    is_prime = True
    
    # Check if num is divisible by any number from 2 to num-1
    for divisor in range(2, num):
        if num % divisor == 0:
            is_prime = False
            break  # No need to check further divisors
    
    if is_prime:
        print(num, end=" ")

print()  # New line at the end
