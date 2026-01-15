# Exercise 1: Movie Night Calculator
# Calculate the total cost of a movie night with formatted output

# Solution:

print("=" * 40)
print("MOVIE NIGHT CALCULATOR")
print("=" * 40)

# Get movie night details (simulating input)
num_tickets = 3
ticket_price = 12.50
num_popcorns = 2
popcorn_price = 8.00
num_drinks = 3
drink_price = 5.50

# Calculate totals
tickets_total = num_tickets * ticket_price
popcorn_total = num_popcorns * popcorn_price
drinks_total = num_drinks * drink_price
subtotal = tickets_total + popcorn_total + drinks_total

# Tax calculation
tax_rate = 0.08
tax_amount = subtotal * tax_rate
grand_total = subtotal + tax_amount

# Cost per person
cost_per_person = grand_total / num_tickets

# Display formatted receipt
print(f"\n{'ITEM':<20} {'QTY':>5} {'PRICE':>10} {'TOTAL':>10}")
print("-" * 45)
print(f"{'Movie Tickets':<20} {num_tickets:>5} {ticket_price:>10.2f} {tickets_total:>10.2f}")
print(f"{'Popcorn':<20} {num_popcorns:>5} {popcorn_price:>10.2f} {popcorn_total:>10.2f}")
print(f"{'Drinks':<20} {num_drinks:>5} {drink_price:>10.2f} {drinks_total:>10.2f}")
print("-" * 45)
print(f"{'Subtotal':<20} {'':<5} {'':<10} {subtotal:>10.2f}")
print(f"{'Tax (8%)':<20} {'':<5} {'':<10} {tax_amount:>10.2f}")
print("=" * 45)
print(f"{'GRAND TOTAL':<20} {'':<5} {'':<10} ${grand_total:>9.2f}")
print(f"\nCost per person: ${cost_per_person:.2f}")
print("=" * 40)
