import pygame
from pygame.surface import Surface

import settings
from game_state import GameState
from objects.field.tile import Tile


class Wall(Tile):
    filename_wall = 'images/wall.png'
    filename_no_wall = 'images/nowall.png'
    image_no_wall = pygame.image.load(filename_no_wall)

    def __init__(self, x: int, y: int, wall_type: int):
        self.type = wall_type
        super().__init__(x, y)
        self.sections = [list()] * 3
        for i in range(3):
            self.sections[i] = [False] * 3
        self.sections[1][1] = True
        if settings.state == GameState.roma:
            self.filename_wall = 'images/roma_state/HappyNewYear/wall.png'
        self.image_wall = pygame.image.load(self.filename_wall)

    def process_draw(self, screen: Surface):
        for i in range(3):
            for j in range(3):
                if self.sections[i][j]:
                    screen.blit(self.image_wall, (self.rect.x + 7 * j, self.rect.y + 7 * i))
                else:
                    screen.blit(self.image_no_wall, (self.rect.x + 7 * j, self.rect.y + 7 * i))
