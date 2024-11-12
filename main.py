# main.py
import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

# Create player
player = Player()

# Instantiate CarManager and Scoreboard
car_manager = CarManager()
score = Scoreboard()

# Control player
screen.listen()
screen.onkeypress(player.move_up, "Up")
screen.onkeypress(player.move_left, "Left")
screen.onkeypress(player.move_right, "Right")
screen.onkeypress(player.move_down, "Down")

# Pausing and restarting
game_is_on = True
game_paused = False


def toggle_pause():
    global game_paused
    game_paused = not game_paused


screen.onkeypress(toggle_pause, "p")  # Press 'P' to pause/resume


def restart_game():
    global game_is_on, game_paused, player, car_manager, score

    # Reset game flags and states
    game_is_on = True
    game_paused = False

    # Clear all cars and reset car manager
    for car in car_manager.all_cars:
        car.hideturtle()
    car_manager.all_cars.clear()
    car_manager.move_increment = 0

    # Reset player position and scoreboard
    player.go_to_start()
    score.clear()
    score.current_level = 1
    score.update_scoreboard()


screen.onkeypress(restart_game, "Escape")  # Press 'Escape' to restart

# Game loop
while True:
    if game_is_on:
        if not game_paused:
            time.sleep(0.05)
            screen.update()

            # Simulate 3D effect by changing the player color
            player.simulate_3d_effect()

            # Game logic
            car_manager.make_car()
            car_manager.move()

            # Detect collision with car
            for car in car_manager.all_cars:
                if player.distance(car) < 21:
                    score.game_over()  # Display game over
                    game_is_on = False  # Pause game until restart
                    break  # Exit for loop to avoid further processing

            # Detect successful crossing and speed up cars
            if player.is_at_finish_line():
                player.go_to_start()
                car_manager.increase_speed()
                score.update_scoreboard()
    else:
        # Wait for Escape key to restart if game is over
        screen.update()

# Detect screen click to exit
screen.exitonclick()
