# From: Zero to AI Agent, Chapter 12, Section 12.2
# File: exercise_1_12_2_solution.py

from langchain_core.tools import Tool

def unit_converter(conversion_request: str) -> str:
    """Convert between common units."""
    try:
        parts = conversion_request.lower().split()
        if len(parts) != 4 or parts[2] != 'to':
            return "Error: Use format '100 meters to feet'"
        
        value = float(parts[0])
        from_unit = parts[1]
        to_unit = parts[3]
        
        # Conversion rates to base units
        conversions = {
            'meters': 1.0, 'feet': 0.3048, 'miles': 1609.34,
            'kilograms': 1.0, 'pounds': 0.453592, 'grams': 0.001,
            'celsius': 'temp', 'fahrenheit': 'temp', 'kelvin': 'temp'
        }
        
        # Temperature conversions
        if from_unit in ['celsius', 'fahrenheit', 'kelvin']:
            if from_unit == 'celsius' and to_unit == 'fahrenheit':
                result = (value * 9/5) + 32
            elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                result = (value - 32) * 5/9
            else:
                return "Temperature conversion not implemented"
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
        
        # Linear conversions
        if from_unit not in conversions or to_unit not in conversions:
            return "Error: Unknown unit"
        
        # Convert through base unit
        base_value = value * conversions[from_unit]
        result = base_value / conversions[to_unit]
        
        return f"{value} {from_unit} = {result:.2f} {to_unit}"
        
    except Exception as e:
        return f"Error: {str(e)}"

# Create the tool
converter_tool = Tool(
    name="UnitConverter",
    func=unit_converter,
    description="Convert units. Format: 'value from_unit to to_unit'"
)

# Test
if __name__ == "__main__":
    print(converter_tool.func("100 meters to feet"))
    print(converter_tool.func("32 fahrenheit to celsius"))
