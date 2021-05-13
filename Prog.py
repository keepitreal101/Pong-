import tkinter as tk
from random import randint

# Constants
limit_height = 500
limit_width = 600
limit_top = [7, 27]
limit_bot = [593, 493]
bg_colour = "black"
initial_score = 0
score_font = 10
ini_ship_length = 60
increment = 15
radius = 8
game_delay = 20
rate = 1.05


class Initial(tk.Canvas):
    def __init__(self):
        super().__init__(width=limit_width, height=limit_height, bg=bg_colour, highlightthickness=0)
        self.create_rectangle(limit_top[0], limit_top[1],
                              limit_bot[0], limit_bot[1], outline="#525d69")  # creates outline
        self.score = 0
        self.create_text(50, 11, text=f"score: {self.score}",
                         tag="score", fill="#fff", font=score_font)  # creates score

        middle_x = 0.5 * (limit_bot[0] - limit_top[0])
        middle_y = 0.5 * (limit_bot[1] - limit_top[1])
        self.ship_co = [[middle_x - ini_ship_length, limit_bot[1] - 40],
                        [middle_x + ini_ship_length, limit_bot[1] - 20]]  # stores the ship coordinates
        self.ship = self.create_rectangle(middle_x - ini_ship_length, limit_bot[1] - 40,
                                          middle_x + ini_ship_length, limit_bot[1] - 20,
                                          fill="white", outline="#525d69", tags="ship")  # creates the ship
        self.bind_all("<Key>", self.press)  # moves the ship on key press

        self.bal_co = [[middle_x - radius, middle_y - radius],
                       [middle_x + radius, middle_y + radius]]  # stores the ball coordinates
        self.bal = self.create_oval(middle_x - radius, middle_y - radius,
                                    middle_x + radius, middle_y + radius,
                                    fill="blue", tags="ship")  # creates the ball
        self.direction = [randint(-3, -1), 3]

        self.game_end = False

        self.after(game_delay, self.action)

    # Changes the ship according to keyboard input
    def press(self, e):
        command = e.keysym
        allowed = ["Left", "Right"]
        lst = {"Left": -1, "Right": 1}
        if command not in allowed:
            return
        left_x = self.ship_co[0][0] + (lst[command] * increment)
        right_x = self.ship_co[1][0] + (lst[command] * increment)
        if left_x < limit_top[0]:
            left_x = limit_top[0]
            right_x = limit_top[0] + (2 * ini_ship_length)
        elif right_x > limit_bot[0]:
            right_x = limit_bot[0]
            left_x = limit_bot[0] - (2 * ini_ship_length)
        self.ship_co[0][0] = left_x
        self.ship_co[1][0] = right_x
        self.coords(self.ship, *self.ship_co[0], *self.ship_co[1])

    # Displays the end result after a game if conditions are met
    def end_game(self):
        if self.bal_co[1][1] < limit_bot[1] - 40:
            return
        self.delete(tk.ALL)
        self.create_text(
            (0.5 * (limit_bot[0] - limit_top[0])),
            (limit_bot[1] - limit_top[1]),
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=14
        )
        self.game_end = True

    # Accommodates for deflections on all four possible surfaces
    def adjust(self):
        moved = False
        if self.direction[1] > 0:
            if self.bal_co[1][1] + 5 >= limit_bot[1] - 40:
                if self.bal_co[0][0] >= self.ship_co[0][0] and self.bal_co[1][0] <= self.ship_co[1][0]:
                    self.direction[1] *= -1 * rate
                    moved = True
        elif self.direction[1] < 0:
            if self.bal_co[0][1] - 5 <= limit_top[1]:
                self.direction[1] *= -1

        if self.direction[0] > 0:
            if self.bal_co[1][0] + 5 >= limit_bot[0]:
                self.direction[0] *= -1 + (randint(-30, 30) / 100)
        elif self.direction[0] < 0:
            if self.bal_co[0][0] - 5 <= limit_top[0]:
                self.direction[0] *= -1 + (randint(-30, 30) / 100)
        if moved:
            self.score += 1
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score}", tag="score")

    # Moves the ball in its direction
    def move_ball(self):
        self.bal_co[0][0] += self.direction[0]
        self.bal_co[1][0] += self.direction[0]
        self.bal_co[0][1] += self.direction[1]
        self.bal_co[1][1] += self.direction[1]
        self.move(self.bal, self.direction[0], self.direction[1])

    # Calls all other functions
    def action(self):
        self.end_game()  # Checks if the game has ended
        if self.game_end:
            return

        self.adjust()  # Adjusts the ball's direction if necessary
        self.move_ball()  # Moves the ball

        self.after(game_delay, self.action)


# Setup and Execution
game = tk.Tk()
game.title("Pong")
game.resizable(False, False)
board = Initial()
board.pack()
game.mainloop()
