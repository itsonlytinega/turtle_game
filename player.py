# player.py
from turtle import Turtle
import random

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 275

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("lightgray")
        self.penup()
        self.go_to_start()

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def reset_position(self):
        """Reset player to the starting position."""
        self.go_to_start()

    def move_up(self):
        new_y = self.ycor() + MOVE_DISTANCE
        if new_y < 290:
            self.goto(self.xcor(), new_y)

    def move_left(self):
        new_x = self.xcor() - MOVE_DISTANCE
        if new_x > -290:
            self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + MOVE_DISTANCE
        if new_x < 290:
            self.goto(new_x, self.ycor())

    def move_down(self):
        new_y = self.ycor() - MOVE_DISTANCE
        if new_y > -290:
            self.goto(self.xcor(), new_y)

    def is_at_finish_line(self):
        return self.ycor() > FINISH_LINE_Y

    def simulate_3d_effect(self):
        color_shades = ["lightgray", "gray", "darkgray", "slategray", "dimgray", "darkslategray"]
        random_color = random.choice(color_shades)
        self.color(random_color)
