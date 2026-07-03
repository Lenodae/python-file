import tkinter as tk
from tkinter import messagebox

BOARD_SIZE = 15
CELL_SIZE = 40
MARGIN = 30
RADIUS = 16


class Gomoku:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("五子棋")
        self.root.resizable(False, False)

        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1  # 1=黑, 2=白
        self.game_over = False
        self.win_coords = []

        canvas_size = BOARD_SIZE * CELL_SIZE + MARGIN * 2
        self.canvas = tk.Canvas(
            self.root, width=canvas_size, height=canvas_size, bg="#DEB887"
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.status_label = tk.Label(
            self.root, text="黑棋先行", font=("Arial", 14)
        )
        self.status_label.pack(pady=5)

        btn = tk.Button(self.root, text="重新开始", command=self.reset)
        btn.pack(pady=5)

        self._draw_board()
        self.root.mainloop()

    def _draw_board(self):
        c = self.canvas
        for i in range(BOARD_SIZE):
            x = MARGIN + i * CELL_SIZE
            # 横线
            c.create_line(MARGIN, x, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, x)
            # 竖线
            c.create_line(x, MARGIN, x, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE)

        # 星位标记
        if BOARD_SIZE == 15:
            for r, c_ in [(3, 3), (3, 7), (3, 11), (7, 3), (7, 7), (7, 11),
                          (11, 3), (11, 7), (11, 11)]:
                x = MARGIN + r * CELL_SIZE
                y = MARGIN + c_ * CELL_SIZE
                self.canvas.create_oval(
                    x - 3, y - 3, x + 3, y + 3, fill="black"
                )

    def on_click(self, event):
        if self.game_over:
            return

        col = round((event.x - MARGIN) / CELL_SIZE)
        row = round((event.y - MARGIN) / CELL_SIZE)

        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return
        if self.board[row][col] != 0:
            return

        self.board[row][col] = self.current_player
        self._draw_piece(row, col)

        if self._check_win(row, col):
            self.game_over = True
            self._highlight_win()
            winner = "黑棋" if self.current_player == 1 else "白棋"
            self.status_label.config(text=f"{winner} 获胜！")
            messagebox.showinfo("游戏结束", f"{winner} 获胜！")
            return

        if self._is_draw():
            self.game_over = True
            self.status_label.config(text="平局！")
            messagebox.showinfo("游戏结束", "平局！")
            return

        self.current_player = 3 - self.current_player
        name = "黑棋" if self.current_player == 1 else "白棋"
        self.status_label.config(text=f"{name} 走")

    def _draw_piece(self, row, col):
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        color = "black" if self.current_player == 1 else "white"
        self.canvas.create_oval(
            x - RADIUS, y - RADIUS,
            x + RADIUS, y + RADIUS,
            fill=color, outline="gray"
        )

    def _check_win(self, row, col):
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            count = 1
            coords = [(row, col)]

            # 正方向
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and \
                    self.board[r][c] == player:
                coords.append((r, c))
                count += 1
                r += dr
                c += dc

            # 反方向
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and \
                    self.board[r][c] == player:
                coords.append((r, c))
                count += 1
                r -= dr
                c -= dc

            if count >= 5:
                self.win_coords = coords
                return True

        return False

    def _highlight_win(self):
        for row, col in self.win_coords:
            x = MARGIN + col * CELL_SIZE
            y = MARGIN + row * CELL_SIZE
            self.canvas.create_oval(
                x - RADIUS + 2, y - RADIUS + 2,
                x + RADIUS - 2, y + RADIUS - 2,
                outline="red", width=3
            )

    def _is_draw(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    def reset(self):
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.win_coords = []
        self.canvas.delete("all")
        self._draw_board()
        self.status_label.config(text="黑棋先行")


if __name__ == "__main__":
    Gomoku()