# From: Zero to AI Agent, Chapter 3, Section 3.3
# maintenance_reminder.py

days_since_maintenance = int(input("Days since last maintenance: "))
has_error_codes = input("Any error codes? (yes/no): ").lower() == "yes"

# Need maintenance if it's been too long OR there are errors
needs_maintenance = days_since_maintenance > 30 or has_error_codes

if not needs_maintenance:
    print("✅ System healthy! No maintenance needed.")
else:
    print("🔧 Maintenance required!")
    if days_since_maintenance > 30:
        print(f"  - It's been {days_since_maintenance} days (recommended: 30)")
    if has_error_codes:
        print("  - Error codes detected")
