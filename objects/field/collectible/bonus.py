import pygame

from objects.field.collectible.collectible import Collectible
from animation import Animation


class Bonus(Collectible):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.animation = Animation(
          ["images/bonus1.png", "images/bonus2.png", "images/bonus3.png", "images/bonus4.png", "images/bonus5.png",
           "images/bonus6.png"], 4)
        self.image = pygame.image.load("images/bonus1.png")

    def process_draw(self, screen: pygame.Surface):
        self.image = self.animation.get_next_frame()
        screen.blit(self.image, self.rect)
