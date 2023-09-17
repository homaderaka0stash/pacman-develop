import pygame

from objects.field.tile import Tile


class Destructible_wall(Tile):

    def __init__(self, x: int, y: int, type: int):
        super().__init__(x, y)
        self.type = type
        if self.type == 1:
            self.filename = 'images/roma_state/destructible_wall1.png'
        elif self.type == 2:
            self.filename = 'images/roma_state/destructible_wall3.png'
        self.state = False
        self.image = pygame.image.load(self.filename)

    def process_collection(self, field_map):
        field_map[self.rect.y // 21][self.rect.x // 21] = Tile(self.rect.x, self.rect.y)

    def image_update(self, state):
        self.state = state
        if self.state:
            if self.type == 1:
                self.filename = 'images/roma_state/destructible_wall2.png'
            elif self.type == 2:
                self.filename = 'images/roma_state/destructible_wall4.png'
            self.image = pygame.image.load(self.filename)
