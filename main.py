import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
MOVE_DISTANCE = 8  # Reduced the player's movement speed
FINISH_LINE_Y = 50
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

# Create the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Sphere Game")
clock = pygame.time.Clock()

# Player Class
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 50
        self.radius = 15  # Ball size
    def go_to_start(self):
        self.x, self.y = WIDTH // 2, HEIGHT - 50
    def reset_position(self):
        self.go_to_start()
    def move_up(self):
        if self.y - MOVE_DISTANCE >= 0:
            self.y -= MOVE_DISTANCE
    def move_left(self):
        if self.x - MOVE_DISTANCE >= 0:
            self.x -= MOVE_DISTANCE
    def move_right(self):
        if self.x + MOVE_DISTANCE <= WIDTH:
            self.x += MOVE_DISTANCE
    def move_down(self):
        if self.y + MOVE_DISTANCE <= HEIGHT:
            self.y += MOVE_DISTANCE
    def is_at_finish_line(self):
        return self.y < FINISH_LINE_Y
    def draw(self):
        draw_sphere(screen, self.x, self.y, self.radius)
