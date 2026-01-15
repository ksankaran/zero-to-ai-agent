# From: Zero to AI Agent, Chapter 3, Section 3.2
# inventory_manager.py
# An AI inventory system making decisions

stock_level = int(input("Current stock level: "))
minimum_required = 50
reorder_point = 100

if stock_level == 0:
    print("🚨 CRITICAL: Out of stock! Emergency order needed!")
elif stock_level < minimum_required:
    print("⚠️ WARNING: Stock critically low!")
    shortage = minimum_required - stock_level
    print(f"Order at least {shortage} units immediately!")
elif stock_level <= reorder_point:
    print("📦 Stock running low. Time to reorder.")
    suggested_order = reorder_point * 2 - stock_level
    print(f"Suggested order: {suggested_order} units")
else:
    print("✅ Stock levels healthy!")
    print(f"You have {stock_level - reorder_point} units above reorder point.")
