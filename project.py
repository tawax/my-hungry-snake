import random
import sys

try:
    import tkinter as tk
except ImportError:
    tk = None

COLS = 20
ROWS = 20
CELL = 25
START_DELAY = 150
MIN_DELAY = 60
COLOR_STEP = 10

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

KEY_BINDINGS = {
    "Up": "Up",
    "Down": "Down",
    "Left": "Left",
    "Right": "Right",
    "w": "Up",
    "s": "Down",
    "a": "Left",
    "d": "Right",
}

# (head color, body color); changes every COLOR_STEP points
SNAKE_PALETTE = [
    ("lime", "green"),
    ("cyan", "deepskyblue"),
    ("yellow", "orange"),
    ("magenta", "purple"),
    ("white", "gray"),
]

INSTRUCTIONS = [
    "W / Up arrow      move up",
    "S / Down arrow    move down",
    "A / Left arrow    move left",
    "D / Right arrow   move right",
    "P                 pause / resume",
    "R                 restart after game over",
]

RULES = [
    "Eat the red food to grow and score.",
    "The snake passes through walls.",
    "Do not hit your own body.",
    f"The snake changes color every {COLOR_STEP} points.",
]


def main():
    if tk is None:
        sys.exit("tkinter is not installed.")
    root = tk.Tk()
    root.title("My Hungry Snake")
    root.resizable(False, False)
    SnakeGame(root)
    root.mainloop()


def next_head(head, direction, cols=COLS, rows=ROWS):
    dx, dy = DIRECTIONS[direction]
    return ((head[0] + dx) % cols, (head[1] + dy) % rows)


def key_to_direction(keysym):
    return KEY_BINDINGS.get(keysym) or KEY_BINDINGS.get(keysym.lower())


def change_direction(current, requested):
    if requested not in DIRECTIONS:
        return current
    cx, cy = DIRECTIONS[current]
    rx, ry = DIRECTIONS[requested]
    if (cx + rx, cy + ry) == (0, 0):
        return current
    return requested


def is_collision(head, snake):
    return head in snake


def place_food(snake, cols=COLS, rows=ROWS):
    free = [(x, y) for x in range(cols) for y in range(rows) if (x, y) not in snake]
    if not free:
        return None
    return random.choice(free)


def speed_for_score(score):
    return max(MIN_DELAY, START_DELAY - score * 3)


def snake_colors(score):
    index = (score // COLOR_STEP) % len(SNAKE_PALETTE)
    return SNAKE_PALETTE[index]


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.high_score = 0
        self.in_menu = True
        self.running = False
        self.paused = False
        self.score = 0
        self.snake = []
        self.food = None
        self.start_button = None

        self.label = tk.Label(root, text="", font=("Arial", 14))
        self.label.pack()
        self.canvas = tk.Canvas(
            root, width=COLS * CELL, height=ROWS * CELL, bg="black", highlightthickness=0
        )
        self.canvas.pack()
        root.bind("<Key>", self.on_key)
        self.show_menu()

    def show_menu(self):
        self.in_menu = True
        width, height = COLS * CELL, ROWS * CELL
        self.canvas.delete("all")
        self.label.config(text="My Hungry Snake")

        self.canvas.create_text(
            width // 2, 40, text="MY HUNGRY SNAKE", fill="lime", font=("Arial", 24, "bold")
        )
        self.canvas.create_text(
            width // 2, 85, text="Controls", fill="white", font=("Arial", 14, "bold")
        )
        for i, line in enumerate(INSTRUCTIONS):
            self.canvas.create_text(
                width // 2, 115 + i * 24, text=line, fill="white", font=("Courier", 12)
            )
        self.canvas.create_text(
            width // 2, 280, text="Rules", fill="white", font=("Arial", 14, "bold")
        )
        for i, line in enumerate(RULES):
            self.canvas.create_text(
                width // 2, 310 + i * 24, text=line, fill="white", font=("Arial", 11)
            )

        self.start_button = tk.Button(
            self.canvas, text="START", font=("Arial", 16, "bold"), width=10,
            command=self.start,
        )
        self.canvas.create_window(width // 2, height - 40, window=self.start_button)

    def start(self):
        if not self.in_menu:
            return
        self.in_menu = False
        if self.start_button is not None:
            self.start_button.destroy()
            self.start_button = None
        self.reset()

    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = "Right"
        self.pending = "Right"
        self.score = 0
        self.food = place_food(self.snake)
        self.running = True
        self.paused = False
        self.draw()
        self.root.after(START_DELAY, self.tick)

    def on_key(self, event):
        key = event.keysym
        if self.in_menu:
            if key in ("Return", "space"):
                self.start()
            return

        direction = key_to_direction(key)
        if direction:
            self.pending = change_direction(self.direction, direction)
        elif key.lower() == "p" and self.running:
            self.paused = not self.paused
            self.draw()
        elif key.lower() == "r" and not self.running:
            self.reset()

    def tick(self):
        if not self.running:
            return
        if not self.paused:
            self.step()
        if self.running:
            self.root.after(speed_for_score(self.score), self.tick)

    def step(self):
        self.direction = self.pending
        head = next_head(self.snake[0], self.direction)
        eating = head == self.food
        body = self.snake if eating else self.snake[:-1]

        if is_collision(head, body):
            self.running = False
            self.high_score = max(self.high_score, self.score)
            self.draw()
            return

        self.snake.insert(0, head)
        if eating:
            self.score += 1
            self.food = place_food(self.snake)
            if self.food is None:
                self.running = False
                self.high_score = max(self.high_score, self.score)
        else:
            self.snake.pop()
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.label.config(text=f"Score: {self.score}   Best: {self.high_score}")

        if self.food:
            self.draw_cell(self.food, "red")
        head_color, body_color = snake_colors(self.score)
        for i, segment in enumerate(self.snake):
            self.draw_cell(segment, head_color if i == 0 else body_color)

        if not self.running:
            self.center_text("Game Over\nPress R to restart")
        elif self.paused:
            self.center_text("Paused\nPress P to resume")

    def draw_cell(self, cell, color):
        x, y = cell
        self.canvas.create_rectangle(
            x * CELL + 1, y * CELL + 1, (x + 1) * CELL - 1, (y + 1) * CELL - 1,
            fill=color, outline=""
        )

    def center_text(self, text):
        self.canvas.create_text(
            COLS * CELL // 2, ROWS * CELL // 2,
            text=text, fill="white", font=("Arial", 22, "bold"), justify="center"
        )


if __name__ == "__main__":
    main()
