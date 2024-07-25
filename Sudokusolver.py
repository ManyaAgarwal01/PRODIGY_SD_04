import tkinter as tk
from tkinter import messagebox

class SudokuGUI:
    def __init__(self, master, grid_size):
        self.master = master
        self.grid_size = grid_size
        self.master.title(f"Sudoku Solver - {self.grid_size}x{self.grid_size}")
        
        self.background_color = "#E0E0E0"  
        self.button_color = "#4CAF50"      
        self.button_text_color = "white"
        
       
        self.frame = tk.Frame(self.master, bg=self.background_color)
        self.frame.pack(padx=10, pady=10)

        
        self.entries = [[None]*self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.entries[i][j] = tk.Entry(self.frame, width=3, font=('Arial', 18, 'bold'), justify='center')
                self.entries[i][j].grid(row=i, column=j, padx=1, pady=1)

        # Solve button
        solve_button = tk.Button(self.frame, text="Solve Sudoku", command=self.solve_sudoku, bg=self.button_color, fg=self.button_text_color)
        solve_button.grid(row=self.grid_size, column=0, columnspan=self.grid_size, pady=10, padx=5, sticky="ew")

        # Clear button
        clear_button = tk.Button(self.frame, text="Clear Grid", command=self.clear_grid, bg=self.button_color, fg=self.button_text_color)
        clear_button.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size, pady=10, padx=5, sticky="ew")

    def solve_sudoku(self):
        puzzle = [[0]*self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.entries[i][j].get()
                if value.isdigit() and 1 <= int(value) <= self.grid_size:
                    puzzle[i][j] = int(value)
                else:
                    puzzle[i][j] = 0  # treat empty or invalid input as 0

        if self.solve(puzzle):
            # Display solved puzzle
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.entries[i][j].delete(0, tk.END)
                    self.entries[i][j].insert(0, puzzle[i][j])
        else:
            # If no solution found, show message
            messagebox.showinfo("No Solution", "This Sudoku puzzle has no solution.")

    def solve(self, puzzle):
        empty = self.find_empty_position(puzzle)
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        for num in range(1, self.grid_size + 1):
            if self.is_valid(puzzle, row, col, num):
                puzzle[row][col] = num

                if self.solve(puzzle):
                    return True

                puzzle[row][col] = 0  # Backtrack

        return False  # No solution found

    def find_empty_position(self, puzzle):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if puzzle[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, puzzle, row, col, num):
        # Check row
        if num in puzzle[row]:
            return False

        # Check column
        if num in [puzzle[i][col] for i in range(self.grid_size)]:
            return False

        # Check subgrid
        subgrid_size = int(self.grid_size ** 0.5)  # size of subgrid (sqrt of grid_size)
        start_row, start_col = subgrid_size * (row // subgrid_size), subgrid_size * (col // subgrid_size)
        for i in range(start_row, start_row + subgrid_size):
            for j in range(start_col, start_col + subgrid_size):
                if puzzle[i][j] == num:
                    return False

        return True

    def clear_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.entries[i][j].delete(0, tk.END)

def main():
    grid_size = int(input("Enter size of Sudoku grid (e.g., 4, 9, 16): "))
    root = tk.Tk()
    sudoku_gui = SudokuGUI(root, grid_size)
    root.mainloop()

if __name__ == "__main__":
    main()
