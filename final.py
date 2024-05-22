import tkinter as tk
from tkinter import messagebox
import math

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.current_player = 'X'
        self.window.resizable(False, False)
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.ai_score = 0
        self.player_score = 0
        self.window.config(bg='#00bfff')
        self.create_menu()
        self.create_board_buttons()
        self.init_scores()
        self.window.mainloop()

    def create_menu(self):
        menu_bar = tk.Menu(self.window)
        self.window.config(menu=menu_bar)

        main_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Menu", menu=main_menu)

        main_menu.add_command(label="New Game", command=self.new_game)
        main_menu.add_separator()
        main_menu.add_command(label="Exit", command=self.window.destroy)

    def create_board_buttons(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, text='', font=('normal', 20), width=6, height=2,
                                   command=lambda row=i, col=j: self.on_button_click(row, col))
                button.grid(row=i + 1, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                if self.current_player == 'X':
                    self.player_score += 1
                else:
                    self.ai_score += 1
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.switch_player()
                self.ai_move()

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_move(self):
        _, best_move = self.minimax(self.board, True)
        if best_move:
            self.board[best_move[0]][best_move[1]] = 'O'
            self.buttons[best_move[0]][best_move[1]].config(text='O')
            if self.check_winner():
                messagebox.showinfo("Game Over", "AI wins!")
                self.ai_score += 1
                self.reset_board()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_board()
            else:
                self.switch_player()
        self.update_score_display()

    def minimax(self, board, is_maximizing, alpha=-math.inf, beta=math.inf):
        if self.check_winner():
            return -1 if is_maximizing else 1, None
        elif self.check_draw():
            return 0, None

        best_score = -math.inf if is_maximizing else math.inf
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O' if is_maximizing else 'X'
                    score, _ = self.minimax(board, not is_maximizing, beta, alpha)
                    board[i][j] = ' '

                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                        alpha = max(alpha, best_score)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)
                        beta = min(beta, best_score)

                    if beta <= alpha:
                        break  # Alpha-beta pruning

        return best_score, best_move

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def check_draw(self):
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j] = ' '
                self.buttons[i][j].config(text=' ')
        self.current_player = 'X'

    def update_score_display(self):
        score_text = f"Player (X): {self.player_score} | AI (O): {self.ai_score}"
        score_label = tk.Label(self.window, text=score_text, font=('normal', 14), pady=20)
        score_label.grid(row=0, column=0, columnspan=3)

    def init_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.update_score_display()

    def new_game(self):
        self.reset_board()
        self.init_scores()

if __name__ == "__main__":
    TicTacToe()



    