import random
import tkinter as tk
from tkinter import messagebox, font

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('2048')
        self.window.config(bg='#faf8ef')
        self.window.resizable(False, False)
        
        # 创建主框架
        self.main_frame = tk.Frame(self.window, bg='#faf8ef', padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # 创建标题和分数框架
        self.header_frame = tk.Frame(self.main_frame, bg='#faf8ef')
        self.header_frame.pack(fill='x', pady=(0, 20))
        
        # 标题
        title_font = font.Font(family='Arial', size=48, weight='bold')
        title = tk.Label(self.header_frame, text='2048', font=title_font, bg='#faf8ef', fg='#776e65')
        title.pack(side='left')
        
        # 分数面板
        self.score_frame = tk.Frame(self.header_frame, bg='#bbada0', padx=15, pady=10, relief='raised')
        self.score_frame.pack(side='right')
        
        score_label = tk.Label(self.score_frame, text='SCORE', font=('Arial', 12, 'bold'), bg='#bbada0', fg='#eee4da')
        score_label.pack()
        
        self.score_value = tk.Label(self.score_frame, text='0', font=('Arial', 20, 'bold'), bg='#bbada0', fg='white')
        self.score_value.pack()
        
        # 游戏网格框架
        self.grid_frame = tk.Frame(self.main_frame, bg='#bbada0', padx=10, pady=10)
        self.grid_frame.pack()
        
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        
        # 创建GUI网格
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(
                    self.grid_frame,
                    bg='#cdc1b4',
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=5, pady=5)
                cell.grid_propagate(False)
                cell_number = tk.Label(
                    master=cell,
                    text="",
                    bg='#cdc1b4',
                    font=("Arial", 36, "bold"),
                    fg='#776e65'
                )
                cell_number.place(relx=0.5, rely=0.5, anchor="center")
                row.append(cell_number)
            self.cells.append(row)
        
        # 绑定键盘事件
        self.window.bind("<Key>", self.key_pressed)
        
        # 初始化游戏
        self.add_new_tile()
        self.add_new_tile()
        self.update_display()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_display(self):
        self.score_value.config(text=str(self.score))
        for i in range(4):
            for j in range(4):
                number = self.grid[i][j]
                if number == 0:
                    self.cells[i][j].config(text="", bg='#cdc1b4')
                else:
                    self.cells[i][j].config(
                        text=str(number),
                        bg=self.get_cell_color(number),
                        fg=self.get_text_color(number)
                    )

    def get_cell_color(self, number):
        colors = {
            0: '#cdc1b4',
            2: '#eee4da',
            4: '#ede0c8',
            8: '#f2b179',
            16: '#f59563',
            32: '#f67c5f',
            64: '#f65e3b',
            128: '#edcf72',
            256: '#edcc61',
            512: '#edc850',
            1024: '#edc53f',
            2048: '#edc22e'
        }
        return colors.get(number, '#ff0000')

    def get_text_color(self, number):
        return '#776e65' if number < 8 else '#f9f6f2'

    def move(self, direction):
        moved = False
        if direction in ['Left', 'Right']:
            for i in range(4):
                line = self.grid[i]
                if direction == 'Right':
                    line = line[::-1]
                new_line = self.merge(line)
                if direction == 'Right':
                    new_line = new_line[::-1]
                if new_line != self.grid[i]:
                    moved = True
                    self.grid[i] = new_line
        else:  # Up or Down
            for j in range(4):
                line = [self.grid[i][j] for i in range(4)]
                if direction == 'Down':
                    line = line[::-1]
                new_line = self.merge(line)
                if direction == 'Down':
                    new_line = new_line[::-1]
                if line != new_line:
                    moved = True
                    for i in range(4):
                        self.grid[i][j] = new_line[i]
        return moved

    def merge(self, line):
        # 移除零
        new_line = [x for x in line if x != 0]
        # 合并相同数字
        for i in range(len(new_line)-1):
            if new_line[i] == new_line[i+1]:
                new_line[i] *= 2
                self.score += new_line[i]
                new_line[i+1] = 0
        # 再次移除零并补齐
        new_line = [x for x in new_line if x != 0]
        new_line.extend([0] * (4 - len(new_line)))
        return new_line

    def key_pressed(self, event):
        if self.game_over:
            return
        
        key_to_direction = {
            'Left': 'Left',
            'Right': 'Right',
            'Up': 'Up',
            'Down': 'Down'
        }
        
        direction = key_to_direction.get(event.keysym)
        if direction:
            moved = self.move(direction)
            if moved:
                self.add_new_tile()
                self.update_display()
                if self.check_game_over():
                    self.game_over = True
                    messagebox.showinfo("游戏结束", f"游戏结束！\n最终得分：{self.score}")

    def check_game_over(self):
        # 检查是否还有空格
        if any(0 in row for row in self.grid):
            return False
        
        # 检查是否还能合并
        for i in range(4):
            for j in range(3):
                if self.grid[i][j] == self.grid[i][j+1]:
                    return False
                if self.grid[j][i] == self.grid[j+1][i]:
                    return False
        return True

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Game2048()
    game.run()