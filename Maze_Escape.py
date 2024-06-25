import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 40
PLAYER_SIZE = 30
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Escape")

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = BLUE

    def move(self, dx, dy, maze):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        if not self.collides_with_wall(new_x, new_y, maze):
            self.rect.x = new_x
            self.rect.y = new_y

    def collides_with_wall(self, x, y, maze):
        cell_x1 = max(0, x // CELL_SIZE)
        cell_y1 = max(0, y // CELL_SIZE)
        cell_x2 = min(len(maze[0]) - 1, (x + PLAYER_SIZE - 1) // CELL_SIZE)
        cell_y2 = min(len(maze) - 1, (y + PLAYER_SIZE - 1) // CELL_SIZE)

        for cy in range(cell_y1, cell_y2 + 1):
            for cx in range(cell_x1, cell_x2 + 1):
                if maze[cy][cx] == 1:
                    return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 1 <= nx < width-1 and 1 <= ny < height-1 and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    # Ensure there is a clear path from start to exit
    maze[height-2][width-2] = 0
    maze[height-2][width-1] = 0
    
    return maze

def draw_text(surface, text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def setup_level(level_data):
    global maze, start_time, time_limit, exit_rect
    maze = generate_maze(level_data["width"], level_data["height"])
    player.rect.topleft = (CELL_SIZE, CELL_SIZE)
    start_time = time.time()
    time_limit = level_data["time_limit"]
    exit_rect = pygame.Rect((level_data["width"] - 2) * CELL_SIZE,
                            (level_data["height"] - 2) * CELL_SIZE,
                            CELL_SIZE * 2, CELL_SIZE)

def main():
    global maze, start_time, time_limit, exit_rect, player
    
    clock = pygame.time.Clock()
    player = Player(CELL_SIZE, CELL_SIZE)
    
    levels = [
        {"width": 20, "height": 15, "time_limit": 60},
        {"width": 20, "height": 15, "time_limit": 50},
        {"width": 20, "height": 15, "time_limit": 40},
    ]

    current_level = 0
    score = 0
    level_complete_time = 0
    level_transition_cooldown = 1  # 1 second cooldown

    setup_level(levels[current_level])

    paused = False
    message = None
    message_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT]:
                dx = -5
            if keys[pygame.K_RIGHT]:
                dx = 5
            if keys[pygame.K_UP]:
                dy = -5
            if keys[pygame.K_DOWN]:
                dy = 5

            player.move(dx, dy, maze)

            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = max(0, time_limit - elapsed_time)

            if remaining_time <= 0:
                message = "Game Over - Time's up!"
                message_time = current_time
                running = False

            if player.rect.colliderect(exit_rect) and current_time - level_complete_time > level_transition_cooldown:
                current_level += 1
                if current_level < len(levels):
                    score += int(remaining_time * 10)
                    setup_level(levels[current_level])
                    message = f"Level {current_level} completed!"
                    message_time = current_time
                    level_complete_time = current_time
                else:
                    message = f"Congratulations! You completed all levels."
                    message_time = current_time
                    running = False

        screen.fill(WHITE)
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 1:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(screen, GREEN, exit_rect)
        draw_text(screen, "EXIT", 20, exit_rect.x + 5, exit_rect.y + 5, WHITE)

        player.draw(screen)

        # Changed these three lines to use RED instead of BLACK
        draw_text(screen, f"Time: {int(remaining_time)}", 30, 10, 10, RED)
        draw_text(screen, f"Score: {score}", 30, WIDTH - 150, 10, RED)
        draw_text(screen, f"Level: {current_level + 1}", 30, WIDTH // 2 - 50, 10, RED)

        if paused:
            draw_text(screen, "PAUSED", 50, WIDTH // 2 - 70, HEIGHT // 2 - 25, RED)

        if message and time.time() - message_time < 3:
            draw_text(screen, message, 30, WIDTH // 2 - 150, HEIGHT // 2 - 15, RED)

        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    screen.fill(WHITE)
    draw_text(screen, message, 40, WIDTH // 2 - 200, HEIGHT // 2 - 50, RED)
    draw_text(screen, f"Final Score: {score}", 30, WIDTH // 2 - 100, HEIGHT // 2 + 50, BLACK)
    pygame.display.flip()
    
    # Wait for a few seconds before quitting
    pygame.time.wait(3000)
    pygame.quit()

if __name__ == "__main__":
    main()