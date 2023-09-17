import pygame
import random
import settings

from game_state import GameState
from objects.ghosts.ghost import Ghost


def state_change(st: GameState):
    settings.state = st


random.seed(version=2)


class Inky(Ghost):
    filename = 'images/inky.png'
    image: pygame.image = pygame.image.load(filename)

    def __init__(self, field_width, start_inky_position):
        super().__init__(field_width, start_inky_position)
