import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
GRAVITY = 1
JUMP_STRENGTH = -15
FPS = 60

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Font setup
font = pygame.font.SysFont(None, 55)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.on_ground = False

    def update(self):
        self.gravity()
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        # Check if player has hit the ground
        if self.rect.y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT
            self.change_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Check horizontal boundaries
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH

        # Check vertical boundaries (ceiling)
        if self.rect.y < 0:
            self.rect.y = 0
            self.change_y = 1  # Start falling down immediately

    def gravity(self):
        if not self.on_ground:
            self.change_y += GRAVITY

    def jump(self):
        if self.on_ground:
            self.change_y = JUMP_STRENGTH
            self.on_ground = False

    def move_left(self):
        self.change_x = -6

    def move_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = random.choice([-2, 2])  # Slower speed

    def update(self):
        self.rect.x += self.change_x
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.change_x *= -1

# Item class
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Level class
class Level:
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.item_list = pygame.sprite.Group()
        self.player = player

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.item_list.update()

    def draw(self, screen):
        screen.fill(BLACK)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.item_list.draw(screen)
        self.player.draw(screen)

# Create platforms for level
def create_level(player):
    level = Level(player)
    platforms = [
        (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
        (150, 480, 150, 10),
        (350, 380, 150, 10),
        (550, 280, 150, 10)
    ]
    for platform in platforms:
        block = Platform(*platform)
        level.platform_list.add(block)

    enemies = [
        (400, 340),
        (600, 240)
    ]
    for enemy_pos in enemies:
        enemy = Enemy(*enemy_pos)
        level.enemy_list.add(enemy)

    items = [
        (250, 450),
        (450, 350),
        (650, 250)
    ]
    for item_pos in items:
        item = Item(*item_pos)
        level.item_list.add(item)

    level.total_items = len(items)  # Store the total number of items in the level
    return level

def main():
    # Create the player
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create the level
    level = create_level(player)

    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()
    game_over = False
    you_won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif not game_over and not you_won and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    player.move_right()
                if event.key == pygame.K_SPACE:
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        if not game_over and not you_won:
            # Update the player and level
            player.update()
            level.update()

            # Check for collisions with platforms
            platform_hits = pygame.sprite.spritecollide(player, level.platform_list, False)
            for platform in platform_hits:
                if player.change_y > 0:  # Falling
                    player.rect.bottom = platform.rect.top
                    player.change_y = 0
                    player.on_ground = True
                elif player.change_y < 0:  # Jumping up
                    player.rect.top = platform.rect.bottom
                    player.change_y = 1  # Start falling down immediately

            # Check for collisions with items
            items_collected = pygame.sprite.spritecollide(player, level.item_list, True)
            for item in items_collected:
                player.score += 1

            # Check for collisions with enemies
            if pygame.sprite.spritecollide(player, level.enemy_list, False):
                game_over = True

            # Check win condition
            if player.score == level.total_items:
                you_won = True

        # Draw everything
        level.draw(screen)
        all_sprites.draw(screen)

        # Display score
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, [10, 10])

        if game_over:
            # Display game over message
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30])
            final_score_text = font.render(f"Final Score: {player.score}", True, WHITE)
            screen.blit(final_score_text, [SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10])

        if you_won:
            # Display you won message
            you_won_text = font.render("You Won!", True, WHITE)
            screen.blit(you_won_text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30])
            final_score_text = font.render(f"Final Score: {player.score}", True, WHITE)
            screen.blit(final_score_text, [SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10])

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
