import pandas as pd
import random

def create_sudoku():
    rows = list(range(1, 10))
    columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

    sudoku = pd.DataFrame(columns=columns, index=rows)  # Create a blank sudoku with letter headers
    
    for col in columns:
        sudoku[col] = random.sample(range(1, 10), 9)    # Fill each column with random numbers

    return sudoku

def format_sudoku(sudoku):
    # Add lines to format the 3x3 grids
    formatted_sudoku = sudoku.copy()
    
    # Add '|' after every 3rd column
    for i, col in enumerate(sudoku.columns):
        if (i + 1) % 3 == 0 and (i + 1) < len(sudoku.columns):
            formatted_sudoku.insert(i + 1, f"{col}_line", '|')

    # Add '-' after every 3rd row
    for i in range(1, len(sudoku) + 1):
        if i % 3 == 0 and i < len(sudoku):
            formatted_sudoku.loc[i + 0.5] = ['-'] * len(formatted_sudoku.columns)
    
    # Sort rows to bring new rows into correct positions
    formatted_sudoku = formatted_sudoku.sort_index().reset_index(drop=True)
    
    return formatted_sudoku

def main():
    # Example usage
    sudoku = create_sudoku()
    print(sudoku)
    formatted_sudoku = format_sudoku(sudoku)
    print(formatted_sudoku)

if __name__ == "__main__":
    main()