import tkinter as tk
from tkinter import messagebox

class Connect4UI:
    def __init__(self, root):
        self.game = Connect4Game()
        self.root = root
        self.root.title("Connect 4")
        self.buttons = []
        self.create_board()
        self.current_turn_label = tk.Label(self.root, text="Player 1's turn", font=("Helvetica", 16))
        self.current_turn_label.grid(row=0, columnspan=7)

    def create_board(self):
        for col in range(7):
            button = tk.Button(self.root, text=str(col+1), command=lambda c=col: self.drop_piece(c))
            button.grid(row=1, column=col, sticky="ew")
            self.buttons.append(button)
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue")
        self.canvas.grid(row=2, column=0, columnspan=7)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                x0, y0 = col * 100, row * 100
                x1, y1 = x0 + 100, y0 + 100
                color = "white" if self.game.board[row][col] == 0 else ("red" if self.game.board[row][col] == 1 else "yellow")
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color)

    def drop_piece(self, column):
        result = self.game.drop_piece(column)
        if result == 'win':
            self.draw_board()
            messagebox.showinfo("Game Over", f"Player {3 - self.game.current_player} wins!")
            self.game.reset_game()
        elif result:
            self.draw_board()
            self.current_turn_label.config(text=f"Player {self.game.current_player}'s turn")
        else:
            messagebox.showwarning("Invalid Move", "This column is full!")

        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4UI(root)
    root.mainloop()
