import pygame
from objects.field.collectible.collectible import Collectible
from animation import Animation
from objects.field.tile import Tile


class Super_coin(Collectible):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.animation = Animation(
          ["images/roma_state/super_coin1.png", "images/roma_state/super_coin2.png",
           "images/roma_state/super_coin3.png", "images/roma_state/super_coin4.png",
           "images/roma_state/super_coin3.png", "images/roma_state/super_coin2.png"], 2)
        self.image = None

    def process_draw(self, screen: pygame.Surface):
        self.image = self.animation.get_next_frame()
        screen.blit(self.image, self.rect)

    def process_collection(self, field_map):
        field_map[self.rect.y // 21][self.rect.x // 21] = Tile(self.rect.x, self.rect.y)
        field_map[self.rect.y // 21][(self.rect.x // 21) + 1] = Tile(self.rect.x + 21, self.rect.y)
