import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Logic Puzzle Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Initialize game state
game_state = MENU
current_level = 1

# Game variables
level_time = 45  # 45 seconds per level
start_time = 0
current_path = []
level_completed = False

# Font
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

def draw_button(text, x, y, w, h, color, text_color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + w/2, y + h/2))
    screen.blit(text_surface, text_rect)

def main_menu():
    global game_state
    screen.fill(WHITE)
    
    title = font.render("Logic Puzzle Game", True, BLACK)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 100))
    
    draw_button("Start Game", 300, 250, 200, 50, GREEN, BLACK)
    draw_button("Quit", 300, 350, 200, 50, RED, BLACK)
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if 300 < mouse_pos[0] < 500 and 250 < mouse_pos[1] < 300:
        if click[0] == 1:
            game_state = PLAYING
    
    if 300 < mouse_pos[0] < 500 and 350 < mouse_pos[1] < 400:
        if click[0] == 1:
            pygame.quit()
            sys.exit()

def draw_grid():
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def generate_level(level):
    return [(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(level + 4)]

def play_level(level):
    global game_state, start_time, current_path, level_completed, current_level

    if start_time == 0:
        start_time = pygame.time.get_ticks()
    
    screen.fill(WHITE)
    draw_grid()
    
    # Generate level if not already generated
    if not hasattr(play_level, 'dots'):
        play_level.dots = generate_level(level)
    
    # Draw dots
    for dot in play_level.dots:
        pygame.draw.circle(screen, BLACK, dot, 10)
    
    # Draw current path
    if len(current_path) > 1:
        pygame.draw.lines(screen, BLUE, False, current_path, 4)
    
    # Draw timer and level
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    remaining_time = max(0, level_time - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(timer_text, (10, 10))
    screen.blit(level_text, (WIDTH - 100, 10))
    
    # Handle mouse events
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if click[0] == 1:
        for dot in play_level.dots:
            if (dot[0] - mouse_pos[0])**2 + (dot[1] - mouse_pos[1])**2 < 100:  # 10^2 radius
                if dot not in current_path:
                    current_path.append(dot)
                    break
    
    # Check for level completion
    if set(current_path) == set(play_level.dots):
        level_completed = True
    
    if level_completed:
        completion_text = font.render("Level Complete!", True, GREEN)
        screen.blit(completion_text, (WIDTH/2 - completion_text.get_width()/2, HEIGHT/2))
        
        if remaining_time > 0:
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait 2 seconds before next level
            current_level += 1
            if current_level > 5:  # 5 levels total
                game_state = GAME_OVER
            else:
                start_time = 0
                current_path = []
                level_completed = False
                # Generate new level
                play_level.dots = generate_level(current_level)
    
    # Check for game over
    if remaining_time == 0:
        game_state = GAME_OVER
        start_time = 0

def game_over():
    global game_state, current_level
    
    screen.fill(WHITE)
    
    if current_level > 5:
        result_text = font.render("Congratulations! You completed all levels!", True, GREEN)
    else:
        result_text = font.render("Game Over!", True, RED)
    
    screen.blit(result_text, (WIDTH/2 - result_text.get_width()/2, HEIGHT/2 - 50))
    
    draw_button("Play Again", 300, 350, 200, 50, GREEN, BLACK)
    draw_button("Quit", 300, 450, 200, 50, RED, BLACK)
    
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if 300 < mouse_pos[0] < 500 and 350 < mouse_pos[1] < 400:
        if click[0] == 1:
            game_state = MENU
            current_level = 1
            current_path.clear()
            if hasattr(play_level, 'dots'):
                del play_level.dots
    
    if 300 < mouse_pos[0] < 500 and 450 < mouse_pos[1] < 500:
        if click[0] == 1:
            pygame.quit()
            sys.exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == MENU:
        main_menu()
    elif game_state == PLAYING:
        if current_level == 1 and len(current_path) == 0:
            start_time = 0
        play_level(current_level)
    elif game_state == GAME_OVER:
        game_over()

    pygame.display.flip()
    clock.tick(60)