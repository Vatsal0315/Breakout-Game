import pygame
import random
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Paddle
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
PADDLE_VELOCITY = 5

# Ball
BALL_RADIUS = 10

# Bricks
BRICK_ROWS = 5
BRICK_COLUMNS = 8
BRICK_WIDTH = SCREEN_WIDTH // BRICK_COLUMNS
BRICK_HEIGHT = 20

# List of brick colors
BRICK_COLORS = [YELLOW, GREEN, ORANGE, RED]

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Initialize the paddle
paddle = pygame.Rect(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# Initialize the ball
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_velocity = [random.choice([-4, 4]), -4]

# Initialize the bricks
def initialize_bricks():
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            color = random.choice(BRICK_COLORS)
            brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
            bricks.append((brick, color))
    return bricks

bricks = initialize_bricks()

# Game variables
score = 0
game_over = False

# Function to reset the game
def reset_game():
    global bricks, score, game_over
    bricks = initialize_bricks()
    score = 0
    game_over = False
    paddle.centerx = SCREEN_WIDTH // 2
    ball.centerx = SCREEN_WIDTH // 2
    ball.centery = SCREEN_HEIGHT // 2
    ball_velocity[0] = random.choice([-4, 4])
    ball_velocity[1] = -4

# Function to display rules
def display_rules():
    font = pygame.font.Font(None, 24)
    rule1 = font.render("Rules of the game:", True, WHITE)
    rule2 = font.render("Use LEFT and RIGHT arrow keys to move the paddle.", True, WHITE)
    rule3 = font.render("Break all bricks to win. Let the ball fall below the paddle and you lose.", True, WHITE)
    rule4 = font.render("Press SPACE to start or restart the game.", True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(rule1, (20, 20))
    screen.blit(rule2, (20, 50))
    screen.blit(rule3, (20, 80))
    screen.blit(rule4, (20, 110))
    pygame.display.flip()

# Initial display of rules
display_rules()

# Flag to indicate if the game should start
start_game = False

# Wait for SPACE key press to start the game
while not start_game:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                start_game = True

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE and game_over:
                reset_game()

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and paddle.left > 0:
            paddle.left -= PADDLE_VELOCITY
        if keys[K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.right += PADDLE_VELOCITY

        # Ball movement
        ball.left += ball_velocity[0]
        ball.top += ball_velocity[1]

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_velocity[0] = -ball_velocity[0]
        if ball.top <= 0:
            ball_velocity[1] = -ball_velocity[1]
        if ball.bottom >= SCREEN_HEIGHT:
            game_over = True

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_velocity[1] = -ball_velocity[1]

        # Ball collision with bricks
        for brick, color in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove((brick, color))
                ball_velocity[1] = -ball_velocity[1]
                score += 1
                break

        # Check if all bricks are destroyed
        if not bricks:
            reset_game()

    # Clear the screen
    screen.fill(BLACK)

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Score: {score}", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        restart_text = font.render("Press SPACE to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(restart_text, restart_rect)
    else:
        pygame.draw.rect(screen, GREEN, paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
