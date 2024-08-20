import pandas as pd
import random

# Rules of Sudoku!
# 1. Each row must have the numbers 1-9 (no repeats)
# 2. Each column must have the numbers 1-9 (no repeats)
# 3. Each 3x3 subgrid must have the numbers 1-9 (no repeats)

def create_sudoku():
    rows = list(range(1, 10))
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    sudoku = pd.DataFrame(columns=columns, index=rows)  # Create a blank sudoku with letter headers
    
    for col in columns:
        sudoku[col] = random.sample(range(1, 10), 9)    # Fill each column with random numbers

    return sudoku

def format_sudoku(sudoku):
    # Print the sudoku in a more readable or sudoku-esque format
    formatted_sudoku = sudoku.to_string(index=False, header=False)
    formatted_sudoku = formatted_sudoku.replace('  ', ' | ', 3)  # Add vertical lines between 3x3 subgrids
    formatted_sudoku = formatted_sudoku.replace(' ', '  ')  # Add extra space between numbers
    formatted_sudoku = formatted_sudoku.replace('\n', '\n\n')  # Add extra line between rows
    # Add 3x3 subgrids
    
    return formatted_sudoku

def main():
    # Example usage
    sudoku = create_sudoku()
    print(sudoku)
    formatted_sudoku = format_sudoku(sudoku)
    print(formatted_sudoku)

if __name__ == "__main__":
    main()