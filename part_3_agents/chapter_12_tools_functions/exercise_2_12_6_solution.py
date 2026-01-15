# From: Zero to AI Agent, Chapter 12, Section 12.6
# File: exercise_2_12_6_solution.py

def smart_data_processor(data_string: str, max_rows: int = 1000, max_cols: int = 100) -> str:
    """Process data with multiple fallback parsing strategies."""
    
    if not data_string:
        return "Error: No data provided"
    
    lines = data_string.strip().split('\n')
    
    # Try different separators in order
    separators = [
        (',', 'CSV'),
        ('\t', 'TSV'),
        (' ', 'Space-separated'),
        ('|', 'Pipe-separated')
    ]
    
    for separator, format_name in separators:
        try:
            # Try to parse with current separator
            parsed_data = []
            for line in lines:
                if line.strip():  # Skip empty lines
                    row = line.split(separator)
                    parsed_data.append(row)
            
            if not parsed_data:
                continue
            
            # Validation
            num_rows = len(parsed_data)
            num_cols = len(parsed_data[0]) if parsed_data else 0
            
            # Check if all rows have same number of columns
            consistent = all(len(row) == num_cols for row in parsed_data)
            
            if not consistent:
                continue  # Try next separator
            
            # Validate size limits
            if num_rows > max_rows:
                return f"Error: Too many rows ({num_rows}). Maximum allowed: {max_rows}"
            
            if num_cols > max_cols:
                return f"Error: Too many columns ({num_cols}). Maximum allowed: {max_cols}"
            
            # Success!
            return f"""Successfully parsed as {format_name}:
- Rows: {num_rows}
- Columns: {num_cols}
- First row: {parsed_data[0]}
- Data preview: {parsed_data[:3]}"""
            
        except Exception:
            continue  # Try next separator
    
    # If all parsing attempts failed
    sample = data_string[:200] + "..." if len(data_string) > 200 else data_string
    return f"""Error: Could not parse data.

Tried formats: CSV, TSV, Space-separated, Pipe-separated

Expected format examples:
- CSV: name,age,city
- TSV: name[TAB]age[TAB]city
- Space: name age city

Your data sample: {sample}"""

# Test the processor
print("SMART DATA PROCESSOR TEST")
print("=" * 50)

test_data = [
    "name,age,city\nJohn,30,NYC\nJane,25,LA",  # CSV
    "name\tage\tcity\nJohn\t30\tNYC",          # TSV
    "name age city\nJohn 30 NYC",               # Space-separated
    "invalid;;;data;;;format",                  # Invalid
    "",                                          # Empty
]

for i, data in enumerate(test_data, 1):
    print(f"\nTest {i}:")
    print(f"Input: {data[:50]}...")
    result = smart_data_processor(data)
    print(f"Result: {result[:200]}")
