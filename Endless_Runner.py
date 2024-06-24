import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arcade Endless Runner")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player
player_width = 50
player_height = 50
player_x = WIDTH // 4
player_y = HEIGHT - player_height - 10
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Game variables
clock = pygame.time.Clock()
score = 0
game_speed = 5
player_speed_increase_interval = 500  # Increase player speed every 500 points
speed_increase_interval = 750  # Increase game speed every 750 points

# Obstacles
obstacles = []
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacle_frequency = 60  # frames

# Power-ups
powerups = []
powerup_width = 30
powerup_height = 30
powerup_speed = 5
powerup_frequency = 180  # frames

def draw_player(player):
    pygame.draw.rect(screen, BLUE, player)

def create_obstacle():
    lane = random.randint(0, 2)
    x = WIDTH + obstacle_width
    y = lane * (HEIGHT // 3) + (HEIGHT // 6) - (obstacle_height // 2)
    obstacle = pygame.Rect(x, y, obstacle_width, obstacle_height)
    obstacles.append(obstacle)

def create_powerup():
    lane = random.randint(0, 2)
    x = WIDTH + powerup_width
    y = lane * (HEIGHT // 3) + (HEIGHT // 6) - (powerup_height // 2)
    powerup = pygame.Rect(x, y, powerup_width, powerup_height)
    powerups.append(powerup)

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

def draw_powerups():
    for powerup in powerups:
        pygame.draw.rect(screen, GREEN, powerup)

def move_obstacles():
    for obstacle in obstacles:
        obstacle.x -= obstacle_speed
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle.x > -obstacle_width]

def move_powerups():
    for powerup in powerups:
        powerup.x -= powerup_speed
    powerups[:] = [powerup for powerup in powerups if powerup.x > -powerup_width]

def check_collision():
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return True
    return False

def collect_powerups():
    global score
    for powerup in powerups:
        if player.colliderect(powerup):
            powerups.remove(powerup)
            score += 10

def increase_speed():
    global game_speed, obstacle_speed, powerup_speed, player_speed
    game_speed += 0.5
    obstacle_speed = game_speed
    powerup_speed = game_speed
    player_speed += 0.5

running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Reset the game
            game_over = False
            score = 0
            game_speed = 5
            obstacle_speed = game_speed
            powerup_speed = game_speed
            player_speed = 5
            player.y = HEIGHT - player_height - 10
            obstacles.clear()
            powerups.clear()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_height:
            player.y += player_speed

        # Create obstacles and power-ups
        if pygame.time.get_ticks() % obstacle_frequency == 0:
            create_obstacle()
        if pygame.time.get_ticks() % powerup_frequency == 0:
            create_powerup()

        # Move obstacles and power-ups
        move_obstacles()
        move_powerups()

        # Check for collisions and collect power-ups
        if check_collision():
            game_over = True
        collect_powerups()

        # Increase speed based on score
        if score > 0 and score % speed_increase_interval == 0:
            increase_speed()

        score += 1

    # Draw everything
    screen.fill(WHITE)
    draw_player(player)
    draw_obstacles()
    draw_powerups()

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Display game speed
    speed_text = font.render(f"Speed: {game_speed:.1f}", True, BLACK)
    screen.blit(speed_text, (10, 50))

    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
        
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press SPACE to restart", True, BLACK)
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + game_over_text.get_height()))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
