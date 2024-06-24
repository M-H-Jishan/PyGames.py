import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Player
player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 5

# Enemy
enemy_width = 50
enemy_height = 50
enemy_speed = 3
enemies = []

# Bullet
bullet_width = 5
bullet_height = 15
bullet_speed = 7
bullets = []

# Font for text
font_large = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 36)

# Game state
game_over = False
score = 0

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                player_x = width // 2 - player_width // 2
                enemies.clear()
                bullets.clear()
                score = 0

    if not game_over:
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_width:
            player_x += player_speed

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.randint(1, 60) == 1:
            enemies.append([random.randint(0, width - enemy_width), 0])

        # Move enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            if enemy[1] > height:
                enemies.remove(enemy)

        # Check for collisions
        for enemy in enemies[:]:
            # Enemy-bullet collision
            for bullet in bullets[:]:
                if (enemy[0] < bullet[0] + bullet_width and
                    enemy[0] + enemy_width > bullet[0] and
                    enemy[1] < bullet[1] + bullet_height and
                    enemy[1] + enemy_height > bullet[1]):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 10
                    break
            
            # Enemy-player collision
            if (enemy[0] < player_x + player_width and
                enemy[0] + enemy_width > player_x and
                enemy[1] < player_y + player_height and
                enemy[1] + enemy_height > player_y):
                game_over = True

    # Draw everything
    window.fill(BLACK)
    if not game_over:
        pygame.draw.rect(window, WHITE, (player_x, player_y, player_width, player_height))
        for enemy in enemies:
            pygame.draw.rect(window, RED, (enemy[0], enemy[1], enemy_width, enemy_height))
        for bullet in bullets:
            pygame.draw.rect(window, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))
        
        # Display score during gameplay
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        window.blit(score_text, (10, 10))
    else:
        game_over_text = font_large.render("GAME OVER", True, WHITE)
        score_text = font_small.render(f"Final Score: {score}", True, WHITE)
        restart_text = font_small.render("Press R to restart", True, WHITE)
        
        window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height()))
        window.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 + score_text.get_height()))
        window.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + score_text.get_height() * 3))

    pygame.display.update()
    clock.tick(60)

pygame.quit()