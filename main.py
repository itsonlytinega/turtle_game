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


# CarManager Class
class CarManager:
    def __init__(self):
        self.all_cars = []
        self.move_increment = 0  # This controls the speed of cars
    def make_car(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:
            car = {"x": WIDTH, "y": random.randint(100, HEIGHT - 100), "width": 40, "height": 20, "color": random.choice(COLORS)}
            self.all_cars.append(car)
    def move(self):
        for car in self.all_cars:
            car["x"] -= (1 + self.move_increment)  # Slower car movement
            if car["x"] < -40:
                self.all_cars.remove(car)
    def increase_speed(self):
        self.move_increment += 1  # Cars get faster as the level increases

# Scoreboard Class
class Scoreboard:
    def __init__(self):
        self.current_level = 1
        self.score = 0
        self.font = pygame.font.SysFont("Courier", 20, bold=True)
    def update_scoreboard(self):
        level_text = self.font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        screen.blit(level_text, (-220, 20))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # Score display
        screen.blit(score_text, (WIDTH - 150, 20))

    def game_over(self):
        game_over_text = self.font.render(f"GAME OVER! Your Score: {self.score}", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        restart_text = self.font.render("Press 'R' to Restart", True, (255, 255, 255))
        screen.blit(restart_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))

    def reset(self):
        self.current_level = 1
        self.score = 0  # Reset score when restarting

    def increase_score(self):
        self.score += 10  # Increase score as the player progresses

