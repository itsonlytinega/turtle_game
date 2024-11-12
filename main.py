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

# Function to draw the sphere
def draw_sphere(surface, center_x, center_y, radius):
    pygame.draw.circle(surface, (150, 150, 150), (center_x, center_y), radius)
    pygame.draw.circle(surface, (100, 100, 100), (center_x, center_y), int(radius * 0.7))
    pygame.draw.circle(surface, (50, 50, 50), (center_x, center_y), int(radius * 0.5))

# Game Loop
def game_loop():
    screen_paused = False
    game_over = False  # Track if the game is over
    player = Player()
    car_manager = CarManager()
    score = Scoreboard()

    while True:  # Keep the game loop running even after the game over
        screen.fill((0, 0, 0))  # Fill the screen with black

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the program

        # Key Press Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Toggle pause on spacebar
            if not game_over:  # Prevent toggling pause if game is over
                screen_paused = not screen_paused
                pygame.time.delay(300)  # Delay to avoid toggle on a single keypress

        if not screen_paused and not game_over:
            if keys[pygame.K_UP]:
                player.move_up()
            if keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_RIGHT]:
                player.move_right()
            if keys[pygame.K_DOWN]:
                player.move_down()

            if keys[pygame.K_r]:  # Restart the game if 'R' is pressed
                player.reset_position()
                car_manager.all_cars.clear()
                car_manager.move_increment = 0
                score.reset()
                game_over = False  # Reset game over flag
                
 # Check for collisions
            for car in car_manager.all_cars:
                car_rect = pygame.Rect(car["x"], car["y"], car["width"], car["height"])
                player_rect = pygame.Rect(player.x - player.radius, player.y - player.radius, player.radius * 2, player.radius * 2)
                if car_rect.colliderect(player_rect):
                    score.game_over()  # Display game over
                    game_over = True  # Set game over state
                    break

            # Detect successful crossing and speed up cars
            if player.is_at_finish_line():
                player.reset_position()  # Reset player only when crossing finish line
                car_manager.increase_speed()  # Increase speed of cars
                score.current_level += 1  # Increase level
                score.increase_score()  # Increase score

            # Draw the player and simulate 3D effect
            player.draw()

            # Move cars
            car_manager.make_car()
            car_manager.move()

            # Draw cars
            for car in car_manager.all_cars:
                pygame.draw.rect(screen, car["color"], (car["x"], car["y"], car["width"], car["height"]))

            # Update scoreboard
            score.update_scoreboard()

        else:
            # If the game is over, show the "Game Over" message
            if game_over:
                score.game_over()
            # Display pause message only if the game is paused
            elif screen_paused:
                pause_text = score.font.render("PAUSED - Press Space to Resume", True, (255, 255, 255))
                screen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2))

        # Update the display
        pygame.display.update()

        # Control the frame rate (reduce the FPS to slow down the game)
        clock.tick(30)  # Reduced the FPS for slower game speed

        # Restart after pressing 'R' after game over
        if game_over and keys[pygame.K_r]:
            game_loop()  # Restart the game loop

# Run the game loop
game_loop()
