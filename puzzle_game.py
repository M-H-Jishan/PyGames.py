#imcomplete



import pygame
import sys
import os
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("2D Puzzle Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load default image
default_image_path = "default_image.jpg"
default_image = pygame.image.load(default_image_path)
default_image = pygame.transform.scale(default_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Function to divide image into puzzle pieces
def divide_image(image, rows, cols):
    piece_width = image.get_width() // cols
    piece_height = image.get_height() // rows
    puzzle_pieces = []
    for y in range(rows):
        for x in range(cols):
            left = x * piece_width
            upper = y * piece_height
            right = left + piece_width
            lower = upper + piece_height
            piece_rect = pygame.Rect(left, upper, piece_width, piece_height)
            piece_image = image.subsurface(piece_rect)
            puzzle_pieces.append((piece_image, piece_rect))
    return puzzle_pieces

# Function to shuffle puzzle pieces
def shuffle_pieces(pieces):
    random.shuffle(pieces)

# Function to draw puzzle pieces on the game window
def draw_pieces(pieces):
    for piece_image, piece_rect in pieces:
        window.blit(piece_image, piece_rect)

# Function to check if puzzle is solved
def is_solved(pieces):
    return all(pieces[i][1] == (i % COLS * piece_width, i // COLS * piece_height, piece_width, piece_height) for i in range(len(pieces)))

# Main game loop
def main():
    global ROWS, COLS, piece_width, piece_height
    running = True
    dragging = False
    selected_piece = None
    clock = pygame.time.Clock()

    # Default game state
    image = default_image
    ROWS, COLS = 4, 4
    pieces = divide_image(image, ROWS, COLS)
    shuffle_pieces(pieces)

    while running:
        window.fill(WHITE)
        window.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, (piece_image, piece_rect) in enumerate(pieces):
                        if piece_rect.collidepoint(mouse_pos):
                            dragging = True
                            selected_piece = i
                            offsetX = piece_rect.x - mouse_pos[0]
                            offsetY = piece_rect.y - mouse_pos[1]
                            break
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    selected_piece = None
            elif event.type == MOUSEMOTION:
                if dragging:
                    mouse_pos = pygame.mouse.get_pos()
                    pieces[selected_piece] = (pieces[selected_piece][0], pieces[selected_piece][1].move(mouse_pos[0] + offsetX - pieces[selected_piece][1].x, mouse_pos[1] + offsetY - pieces[selected_piece][1].y))

        draw_pieces(pieces)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
