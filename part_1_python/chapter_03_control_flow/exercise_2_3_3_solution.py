# From: Zero to AI Agent, Chapter 3, Section 3.3
# Exercise 2: Smart Alarm System
# Smart home alarm system with multiple trigger conditions

print("=" * 40)
print("SMART ALARM SYSTEM")
print("=" * 40)

# Get sensor inputs
motion_detected = input("Motion detected? (yes/no): ").lower().strip() == "yes"
is_nighttime = input("Is it nighttime? (yes/no): ").lower().strip() == "yes"
window_opened = input("Window opened? (yes/no): ").lower().strip() == "yes"
nobody_home = input("Is nobody home? (yes/no): ").lower().strip() == "yes"
temperature = float(input("Current temperature (F): "))
silent_mode = input("Silent mode enabled? (yes/no): ").lower().strip() == "yes"

# Check alarm conditions using logical operators
motion_at_night = motion_detected and is_nighttime
window_while_away = window_opened and nobody_home
fire_risk = temperature > 100

# Determine if alarm should trigger
alarm_triggered = (motion_at_night or window_while_away or fire_risk) and not silent_mode

# Display results
print("")
print("SYSTEM STATUS:")
print("-" * 40)

if silent_mode:
    print("SILENT MODE ACTIVE - All alarms disabled")
else:
    if motion_at_night:
        print("[!] Motion detected at night!")
    if window_while_away:
        print("[!] Window opened while nobody home!")
    if fire_risk:
        print(f"[!] High temperature detected: {temperature}F")

    print("")
    if alarm_triggered:
        print("*** ALARM TRIGGERED! ***")
        print("Reason(s):")
        if motion_at_night:
            print("  - Nighttime motion")
        if window_while_away:
            print("  - Window breach while away")
        if fire_risk:
            print("  - Fire risk (high temperature)")
    else:
        print("All clear - No threats detected")

print("=" * 40)
