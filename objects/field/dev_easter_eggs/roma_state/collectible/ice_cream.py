import pygame

from animation import Animation
from objects.field.collectible.collectible import Collectible


class Ice_cream(Collectible):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.animation = Animation(
            ["images/roma_state/HappyNewYear/ice_cream1.png", "images/roma_state/HappyNewYear/ice_cream2.png"], 15)
        self.image = None

    def process_draw(self, screen: pygame.Surface):
        self.image = self.animation.get_next_frame()
        screen.blit(self.image, self.rect)
