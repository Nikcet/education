from tkinter import *
import time
import random

# Берем класс Tk() и пихаем его в переменную, создавая таким образом поле
tk = Tk()
# Заголовок окна
tk.title('Game')
# Запрет на изменение размеров окна
tk.resizable(0, 0)
# Помещаем игровое окно поверх остальных окон
tk.wm_attributes('-topmost', 1)
# Создаем холст
canvas = Canvas(tk, width=500, height=400, highlightthickness=0)
# Говорим холсту, что у каждого видимого элемента будут свои кооржинаты
canvas.pack()
# Обновляем окно с холстом
tk.update()


# Объект шарик
class Ball:
    # Создаем шарик
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score

        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)

        self.canvas.move(self.id, 245, 100)

        starts = [-2, -1, 1, 2]

        random.shuffle(starts)
        self.x = starts[0]
        self.y = -2

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        self.hit_bottom = False

    # Регистрируем касание платформы
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)

        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.score.hit()
                return True
        return False

    # Рисуем шарик
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 120, text='You are dead, pisyun', font=('Courier', 30), fill='red')
        if self.hit_paddle(pos):
            self.y = -3
        if pos[0] <= 0:
            self.x = 3
        elif pos[2] >= self.canvas_width:
            self.x = -3


# Объект платформа
class Paddle:
    # Создаем платформу
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.started = False
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    # Двигаем платформу в право
    def turn_right(self, event):
        self.x = 2

    # Двигается платформу в лево
    def turn_left(self, event):
        self.x = -2

    # Начинаем игру по нажатию клавиши Enter
    def start_game(self, event):
        self.started = True

    # Рисуем платформу
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


# Объект счетчик
class Score:
    # Создаем счетчик
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, font=('Courier', 15), fill=color)

    # Регистрируем попадания
    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)


# Строим саму игру
score = Score(canvas, 'Black')
paddle = Paddle(canvas, 'White')
ball = Ball(canvas, paddle, score, 'Blue')

# Пока шарик не коснется дна поля, играем ;)
while not ball.hit_bottom:
    if paddle.started:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
# Выключаем игру через 2 секунды если проиграли
time.sleep(2)
