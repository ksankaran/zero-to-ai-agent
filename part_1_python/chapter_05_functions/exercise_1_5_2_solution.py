# From: Zero to AI Agent, Chapter 5, Section 5.2
# File: exercise_1_5_2_solution.py

def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between units"""
    # Normalize units to uppercase
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    
    print(f"Converting {value}°{from_unit} to °{to_unit}...")
    
    # Convert to Celsius first (as intermediate)
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    else:
        print(f"Unknown unit: {from_unit}")
        return
    
    # Convert from Celsius to target unit
    if to_unit == 'C':
        result = celsius
    elif to_unit == 'F':
        result = (celsius * 9/5) + 32
    elif to_unit == 'K':
        result = celsius + 273.15
    else:
        print(f"Unknown unit: {to_unit}")
        return
    
    print(f"Result: {value}°{from_unit} = {result:.2f}°{to_unit}")
    return result

# Test the converter
convert_temperature(100, 'C', 'F')  # Boiling water
convert_temperature(32, 'F', 'C')   # Freezing water
convert_temperature(0, 'C', 'K')    # Absolute zero reference
convert_temperature(98.6, 'F', 'C') # Body temperature
