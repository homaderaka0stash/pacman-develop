import pygame

from objects.field.collectible.collectible import Collectible


class Chest(Collectible):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.state = False
        self.filename = 'images/roma_state/HappyNewYear/chest1.png'
        self.image = pygame.image.load(self.filename)

    def image_update(self, state):
        self.state = state
        if self.state:
            self.filename = 'images/roma_state/HappyNewYear/chest2.png'
            self.image = pygame.image.load(self.filename)
