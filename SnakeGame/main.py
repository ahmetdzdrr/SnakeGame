import time

import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Define constants
BLOCK_SIZE = 10
SCREEN_SIZE = (400, 400)
FPS = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Snake Game")

# Create the clock
clock = pygame.time.Clock()


# Define the Food class
class Food:
    def __init__(self):
        self.color = RED
        self.generate_new_position()

    def generate_new_position(self):
        x = random.randint(0, SCREEN_SIZE[0] // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, SCREEN_SIZE[1] // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.position = (x, y)

    def draw(self):
        x, y = self.position
        pygame.draw.rect(screen, self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

# Define the Snake class
class Snake:
    def __init__(self, initial_direction):
        self.direction = initial_direction
        self.segments = [(200, 200), (190, 200), (180, 200)]
        self.color = GREEN
        self.score = 0

    def move(self):
        # Calculate the new head position based on the current direction
        head_x, head_y = self.segments[0]
        if self.direction == "up":
            new_head = (head_x, head_y - BLOCK_SIZE)
        elif self.direction == "down":
            new_head = (head_x, head_y + BLOCK_SIZE)
        elif self.direction == "left":
            new_head = (head_x - BLOCK_SIZE, head_y)
        elif self.direction == "right":
            new_head = (head_x + BLOCK_SIZE, head_y)

        # Insert the new head segment at the beginning of the list
        self.segments.insert(0, new_head)

        # Check for collision with the food
        if self.segments[0] == food.position:
            # If the snake has eaten the food, increase the score and generate a new food
            self.score += 10
            food.generate_new_position()
        else:
            # If the snake has not eaten the food, remove the last segment of the snake
            self.segments.pop()

        # Check for collision with the walls
        if (self.segments[0][0] < 0 or
            self.segments[0][0] >= SCREEN_SIZE[0] or
            self.segments[0][1] < 0 or
            self.segments[0][1] >= SCREEN_SIZE[1]):
            game_over()

        # Check for collision with the body
        for segment in self.segments[1:]:
            if segment == self.segments[0]:
                game_over()

    def draw(self):
        for segment in self.segments:
            x, y = segment
            pygame.draw.rect(screen, self.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

# Define the game over function
def game_over():
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over!", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2))
    screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    time.sleep(2)
    sys.exit()

    # Wait for the user's response
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


# Create the snake and food objects
snake = Snake("right")
food = Food()

# Start the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
            elif event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"

    # Move the snake
    snake.move()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the snake and food
    snake.draw()
    food.draw()

    # Draw the score
    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: {}".format(snake.score), True, WHITE)
    score_rect = score_text.get_rect(bottomright=(SCREEN_SIZE[0] - 10, SCREEN_SIZE[1] - 10))
    screen.blit(score_text, score_rect)

    # Update the display
    pygame.display.flip()

    # Wait for a short time to control the speed of the game
    clock.tick(FPS)

