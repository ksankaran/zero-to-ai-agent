# From: Zero to AI Agent, Chapter 4, Section 4.1
# Exercise 3: Matrix Operations

# 1. Create 3x3 matrix
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print("3x3 Matrix:")
for row in matrix:
    print(row)

# 2. Access center element
center = matrix[1][1]
print(f"Center element: {center}")

# 3. Extract first row
first_row = matrix[0]
print(f"First row: {first_row}")

# 4. Extract last column
last_column = []
for row in matrix:
    last_column.append(row[-1])
print(f"Last column: {last_column}")

# 5. Calculate sum of diagonal elements
diagonal_sum = matrix[0][0] + matrix[1][1] + matrix[2][2]
print(f"Sum of diagonal: {diagonal_sum}")

# 6. Create flattened list
flattened = []
for row in matrix:
    for element in row:
        flattened.append(element)
print(f"Flattened list: {flattened}")
