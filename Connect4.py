import numpy as np
import tkinter as tk
from tkinter import messagebox

class Connect4Game:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)  # 6 rows by 7 columns
        self.current_player = 1

    def drop_piece(self, column): #droping the piece
        if self.board[0][column] != 0:
            return False  # Column is full
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                self.board[row][column] = self.current_player
                if self.check_win(row, column):
                    return 'win'
                if self.check_tie():
                    return 'tie'
                self.current_player = 3 - self.current_player  # Switch player
                return True
        return False

    def check_win(self, row, col):
        def check_direction(dx, dy):
            count = 1
            for d in (1, -1):
                for step in range(1, 4):
                    r, c = row + step * d * dx, col + step * d * dy
                    if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                        count += 1
                    else:
                        break
            return count >= 4

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        return any(check_direction(dx, dy) for dx, dy in directions)
    
    def check_tie(self):
        return not any(0 in row for row in self.board)

    def reset_game(self):
        self.board.fill(0)
        self.current_player = 1
        
#////////////////////////////////////////////////////////////////////////////////////////

class Connect4UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.configure(bg='#333333')
        self.player1_name = None
        self.player2_name = None
        self.player1_score = 0
        self.player2_score = 0
        self.setup_menu()

    def setup_menu(self):
        self.menu_frame = tk.Frame(self.root, bg='#333333')
        self.menu_frame.pack(pady=20)

        tk.Label(self.menu_frame, text="Player 1 Name:", fg='white', bg='#333333', font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5)
        self.player1_entry = tk.Entry(self.menu_frame, font=("Helvetica", 14))
        self.player1_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.menu_frame, text="Player 2 Name:", fg='white', bg='#333333', font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5)
        self.player2_entry = tk.Entry(self.menu_frame, font=("Helvetica", 14))
        self.player2_entry.grid(row=1, column=1, padx=10, pady=5)

        start_button = tk.Button(self.menu_frame, text="Start Game", command=self.start_game, bg='#555555', fg='white', font=("Helvetica", 14), relief='raised', bd=3)
        start_button.grid(row=2, columnspan=2, pady=20)

    def start_game(self):
        self.player1_name = self.player1_entry.get() or "Player 1"
        self.player2_name = self.player2_entry.get() or "Player 2"
        
        self.menu_frame.destroy()
        self.game = Connect4Game()
        self.create_board()
        self.current_turn_label = tk.Label(self.root, text=f"{self.player1_name}'s turn", font=("Helvetica", 16), fg='white', bg='#333333')
        self.current_turn_label.grid(row=0, columnspan=7, pady=10)
        self.score_label = tk.Label(self.root, text=f"{self.player1_name}: {self.player1_score}  {self.player2_name}: {self.player2_score}", font=("Helvetica", 14), fg='white', bg='#333333')
        self.score_label.grid(row=1, columnspan=7, pady=10)

    def create_board(self):
        self.buttons = []
        for col in range(7):
            button = tk.Button(self.root, text=str(col+1), command=lambda c=col: self.drop_piece(c), bg='#444444', fg='white', font=("Helvetica", 14), relief='raised', bd=3)
            button.grid(row=2, column=col, sticky="ew", padx=5, pady=5)
            self.buttons.append(button)
        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue", highlightthickness=0)
        self.canvas.grid(row=3, column=0, columnspan=7)
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                x0, y0 = col * 100, row * 100
                x1, y1 = x0 + 100, y0 + 100
                color = "black" if self.game.board[row][col] == 0 else ("#ff0000" if self.game.board[row][col] == 1 else "#ffff00")
                self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill=color, outline="black")

    def drop_piece(self, column):
        result = self.game.drop_piece(column)
        if result == 'win':
            self.draw_board()
            winner = self.player1_name if self.game.current_player == 2 else self.player2_name
            if self.game.current_player == 2:
                self.player1_score += 1
            else:
                self.player2_score += 1
            self.update_score()
            replay = messagebox.askyesno("Game Over", f"{winner} wins!\nDo you want to play again?")
            if replay:
                self.game.reset_game()
                self.draw_board()
            else:
                self.root.quit()
        elif result == 'tie':
            self.draw_board()
            messagebox.askyesno("Game Over", "It's a tie!\nDo you want to play again?")
            if replay:
                self.game.reset_game()
                self.draw_board()
            else:
                self.root.quit()
        elif result:
            self.draw_board()
            current_player_name = self.player1_name if self.game.current_player == 1 else self.player2_name
            self.current_turn_label.config(text=f"{current_player_name}'s turn")
        else:
            messagebox.showwarning("Invalid Move", "This column is full!")
            self.draw_board()

    def update_score(self):
        self.score_label.config(text=f"{self.player1_name}: {self.player1_score}  {self.player2_name}: {self.player2_score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4UI(root)
    root.mainloop()