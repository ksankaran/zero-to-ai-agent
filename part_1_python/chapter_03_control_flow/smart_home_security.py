# From: Zero to AI Agent, Chapter 3, Section 3.3
# smart_home_security.py

is_door_locked = input("Is the door locked? (yes/no): ").lower() == "yes"
is_alarm_set = input("Is the alarm set? (yes/no): ").lower() == "yes"
is_camera_on = input("Is the camera on? (yes/no): ").lower() == "yes"

if is_door_locked and is_alarm_set and is_camera_on:
    print("🏠✅ House is fully secured! Have a safe trip!")
else:
    print("⚠️ Security check failed!")
    if not is_door_locked:
        print("  - Lock the door")
    if not is_alarm_set:
        print("  - Set the alarm")
    if not is_camera_on:
        print("  - Turn on the camera")
