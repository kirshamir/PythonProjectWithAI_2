from abc import ABC, abstractmethod
import sys
import tkinter as tk
from tkinter import messagebox
from flask import Flask, render_template_string, request, redirect, url_for, session

class TicTacToeBase(ABC):
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def play(self):
        self.print_welcome()
        while True:
            self.display_board()
            move = self.get_move()
            if self.make_move(move):
                if self.check_winner():
                    self.display_board()
                    print(f"Player {self.current_player} wins!")
                    break
                elif self.is_draw():
                    self.display_board()
                    print("It's a draw!")
                    break
                self.switch_player()
            else:
                print("Invalid move. Try again.")

    def print_welcome(self):
        print("Welcome to Tic-Tac-Toe!")

    def display_board(self):
        # To be implemented in subclass if needed
        print(f"\n {self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("---+---+---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("---+---+---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]}\n")

    @abstractmethod
    def get_move(self):
        pass

    def make_move(self, move):
        if 0 <= move < 9 and self.board[move] == ' ':
            self.board[move] = self.current_player
            return True
        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in wins:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                return True
        return False

    def is_draw(self):
        return all(cell != ' ' for cell in self.board)

class TicTacToeConsole(TicTacToeBase):
    def get_move(self):
        try:
            move = int(input(f"Player {self.current_player}, enter your move (1-9): ")) - 1
            return move
        except ValueError:
            return -1

class TicTacToeGUI(TicTacToeBase):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")
        self.buttons = []
        self.status_label = tk.Label(self.root, text=f"Player {self.current_player}'s turn", font=('Arial', 14))
        self.status_label.grid(row=3, column=0, columnspan=3)
        for i in range(9):
            btn = tk.Button(self.root, text=' ', width=6, height=3, font=('Arial', 24),
                            command=lambda idx=i: self.on_button_click(idx))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def get_move(self):
        # Not used in GUI, moves handled by button callbacks
        pass

    def on_button_click(self, idx):
        if self.board[idx] == ' ':
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player)
            if self.check_winner():
                self.status_label.config(text=f"Player {self.current_player} wins!")
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.root.quit()
            elif self.is_draw():
                self.status_label.config(text="It's a draw!")
                messagebox.showinfo("Game Over", "It's a draw!")
                self.root.quit()
            else:
                self.switch_player()
                self.status_label.config(text=f"Player {self.current_player}'s turn")
        else:
            messagebox.showwarning("Invalid Move", "Cell already taken!")

    def play(self):
        self.root.mainloop()

class TicTacToeWeb(TicTacToeBase):
    def __init__(self):
        super().__init__()
        self.app = Flask(__name__)
        self.app.secret_key = 'tic-tac-toe-secret'
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', methods=['GET', 'POST'])
        def index():
            if 'board' not in session:
                session['board'] = [' '] * 9
                session['current_player'] = 'X'
            board = session['board']
            current_player = session['current_player']
            winner = self.check_winner_board(board)
            draw = self.is_draw_board(board)
            message = None
            if winner:
                message = f"Player {current_player} wins!"
            elif draw:
                message = "It's a draw!"
            return render_template_string(self.html_template(), board=board, current_player=current_player, message=message)

        @self.app.route('/move/<int:idx>')
        def move(idx):
            board = session.get('board', [' '] * 9)
            current_player = session.get('current_player', 'X')
            if board[idx] == ' ' and not self.check_winner_board(board) and not self.is_draw_board(board):
                board[idx] = current_player
                session['board'] = board
                if self.check_winner_board(board) or self.is_draw_board(board):
                    pass
                else:
                    session['current_player'] = 'O' if current_player == 'X' else 'X'
            return redirect(url_for('index'))

        @self.app.route('/reset')
        def reset():
            session.pop('board', None)
            session.pop('current_player', None)
            return redirect(url_for('index'))

    def html_template(self):
        with open('tic_tac_toe.html', 'r', encoding='utf-8') as f:
            return f.read()

    def check_winner_board(self, board):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for line in wins:
            if board[line[0]] == board[line[1]] == board[line[2]] != ' ':
                return True
        return False

    def is_draw_board(self, board):
        return all(cell != ' ' for cell in board)

    def get_move(self):
        # Not used in web, moves handled by HTTP requests
        pass

    def play(self):
        self.app.run(debug=True)

def play_console():
    game = TicTacToeConsole()
    game.play()

def play_gui():
    game = TicTacToeGUI()
    game.play()

def play_web():
    game = TicTacToeWeb()
    game.play()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [console|gui|web]")
        return
    mode = sys.argv[1].lower()
    if mode == "console":
        play_console()
    elif mode == "gui":
        play_gui()
    elif mode == "web":
        play_web()
    else:
        print(f"Unknown mode: {mode}. Use 'console', 'gui', or 'web'.")

if __name__ == "__main__":
    main()
