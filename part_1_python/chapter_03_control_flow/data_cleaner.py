# From: Zero to AI Agent, Chapter 3, Section 3.6
# data_cleaner.py

print("📊 Data Cleaning System")
print("Processing sensor readings (ignoring invalid values)...\n")

readings = [23.5, -999, 24.1, -999, 22.8, 25.0, -999, 23.9]
clean_data = []
skipped = 0

for reading in readings:
    if reading == -999:  # -999 indicates a sensor error
        skipped += 1
        continue  # Skip this bad reading
    
    # This code only runs for valid readings
    clean_data.append(reading)
    print(f"✅ Processed: {reading}°C")

print(f"\n📈 Summary:")
print(f"Valid readings: {len(clean_data)}")
print(f"Skipped errors: {skipped}")
print(f"Clean data: {clean_data}")
