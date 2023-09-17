import pygame
from pygame import Rect
from pygame.surface import Surface


class Tile:
    filename = 'images/tile.png'
    image = pygame.image.load(filename)

    def __init__(self, x: int, y: int):
        self.rect: Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def process_draw(self, screen: Surface):
        """Draw the tile into the screen"""
        screen.blit(self.image, self.rect)
