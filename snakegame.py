from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
INITIAL_SPEED = 200  # Slower speed
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

walls_enabled = True
speed = INITIAL_SPEED

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global score, speed

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

        # Increase speed every 5 points
        if score % 5 == 0 and speed > 50:
            speed -= 10
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if direction != opposites.get(new_direction):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if walls_enabled:
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True
    else:
        # Wrap around screen
        if x < 0:
            x = GAME_WIDTH - SPACE_SIZE
        elif x >= GAME_WIDTH:
            x = 0
        if y < 0:
            y = GAME_HEIGHT - SPACE_SIZE
        elif y >= GAME_HEIGHT:
            y = 0
        snake.coordinates[0] = [x, y]

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 30, font=("Arial", 24), text="Game Over!", fill="red")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 10, font=("Arial", 16), text="Restarting in 3 seconds...", fill="white")
    window.after(3000, restart_game)

def restart_game():
    global snake, food, direction, score, speed

    canvas.delete(ALL)
    direction = 'down'
    score = 0
    speed = INITIAL_SPEED
    label.config(text="Score: 0")

    snake = Snake()
    food = Food()
    window.after(speed, next_turn, snake, food)

# --- Tkinter Setup ---
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=("Arial", 20))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT + 70}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

snake = Snake()
food = Food()
window.after(speed, next_turn, snake, food)

window.mainloop()