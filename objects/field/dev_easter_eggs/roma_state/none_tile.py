import pygame

from objects.field.tile import Tile


class None_tile(Tile):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def process_draw(self, screen: pygame.Surface):
        pass
