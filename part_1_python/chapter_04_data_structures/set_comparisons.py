# From: Zero to AI Agent, Chapter 4, Section 4.5
# set_comparisons.py - Subset and superset operations

# AI technology hierarchy
ml_basics = {"Python", "Statistics", "Linear Algebra"}
ml_advanced = {"Python", "Statistics", "Linear Algebra", "Deep Learning", "NLP"}
data_science = {"Python", "Statistics", "SQL", "Visualization"}

# Is ml_basics a subset of ml_advanced?
print(f"ML basics ⊆ ML advanced? {ml_basics.issubset(ml_advanced)}")
print(f"ML basics ⊆ ML advanced? {ml_basics <= ml_advanced}")  # Alternative

# Is ml_advanced a superset of ml_basics?
print(f"ML advanced ⊇ ML basics? {ml_advanced.issuperset(ml_basics)}")
print(f"ML advanced ⊇ ML basics? {ml_advanced >= ml_basics}")  # Alternative

# Are ml_basics and data_science disjoint (no common elements)?
print(f"ML basics ∩ Data Science = ∅? {ml_basics.isdisjoint(data_science)}")
# False, because they share Python and Statistics

# Proper subset (subset but not equal)
print(f"ML basics ⊂ ML advanced? {ml_basics < ml_advanced}")
print(f"ML basics = ML basics? {ml_basics == ml_basics}")

# Practical example: Permission checking
user_permissions = {"read", "write", "execute"}
required_permissions = {"read", "write"}
admin_permissions = {"read", "write", "execute", "delete", "admin"}

# Check if user has all required permissions
has_access = required_permissions.issubset(user_permissions)
print(f"\nUser has required permissions? {has_access}")

# Check if user is admin (has all admin permissions)
is_admin = user_permissions == admin_permissions
print(f"User is admin? {is_admin}")

# Check if user has ANY admin permission
has_some_admin = not user_permissions.isdisjoint(admin_permissions)
print(f"User has some admin permissions? {has_some_admin}")
