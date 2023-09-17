import pygame
import random

from game_state import GameState

import settings
from objects.field.teleport import Teleport
from objects.field.wall import Wall
from objects.ghosts.ghost_state import GhostState
from settings import pixel_tile


def state_change(st: GameState):
    settings.state = st


random.seed(version=2)


class Ghost:
    filename = 'images/dead_ghosha.png'
    image: pygame.image = pygame.image.load(filename)
    dead_img_path = 'images/dead_ghosha.png'
    dead_image: pygame.image = pygame.image.load(dead_img_path)

    def __init__(self, field_width, start_position):
        self.field_width = field_width
        self.state = GhostState.is_stop
        self.Ghost_speed = 3
        self.dir = "up"
        self.rot_image: pygame.image = pygame.image.load(self.filename)
        self.rect: pygame.Rect = self.image.get_rect()
        self.start_pos = start_position
        self.pos = start_position
        self.rect.x = self.pos[0] * pixel_tile
        self.rect.y = self.pos[1] * pixel_tile
        self.speed = [0, 0]

    def change_speed(self, field):

        if self.state == GhostState.is_stop:
            pos0 = self.rect.x // pixel_tile
            pos1 = self.rect.y // pixel_tile

            self.state = GhostState.is_moving

            if self.dir == "up":
                if not isinstance(field.field[pos1 - 1][pos0], Wall):
                    self.speed = [0, -self.Ghost_speed]
                    self.rot_image = pygame.transform.rotate(self.image, 0)
                else:
                    self.state = GhostState.is_stop
                    self.speed = [0, 0]

            elif self.dir == "down":
                if not isinstance(field.field[pos1 + 1][pos0], Wall):
                    self.speed = [0, self.Ghost_speed]
                    self.rot_image = pygame.transform.rotate(self.image, 0)
                else:
                    self.state = GhostState.is_stop
                    self.speed = [0, 0]

            elif self.dir == "left":
                if not isinstance(field.field[pos1][pos0 - 1], Wall):
                    self.speed = [-self.Ghost_speed, 0]
                    self.rot_image = pygame.transform.rotate(self.image, 0)
                else:
                    self.state = GhostState.is_stop
                    self.speed = [0, 0]

            elif self.dir == "right":
                if not isinstance(field.field[pos1][pos0 + 1], Wall):
                    self.speed = [self.Ghost_speed, 0]
                    self.rot_image = pygame.transform.rotate(self.image, 0)
                else:
                    self.state = GhostState.is_stop
                    self.speed = [0, 0]

            elif self.dir == "no":
                self.state = GhostState.is_stop
                self.speed = [0, 0]

    def process_logic(self, field):
        """Process game logic of the Pacman"""

        pos0 = self.rect.x // pixel_tile
        pos1 = self.rect.y // pixel_tile

        # flag = [False, False, False, False]  # up, down, left, right
        # counter = 0

        if self.state == GhostState.is_stop:
            available_dirs = []

            if not isinstance(field.field[pos1 - 1][pos0], Wall) and self.dir != "down":
                available_dirs.append("up")
            if not isinstance(field.field[pos1 + 1][pos0], Wall) and self.dir != "up":
                available_dirs.append("down")
            if not isinstance(field.field[pos1][pos0 - 1], Wall) and self.dir != "right":
                available_dirs.append("left")
            if not isinstance(field.field[pos1][pos0 + 1], Wall) and self.dir != "left":
                available_dirs.append("right")

            self.dir = random.choice(available_dirs)

        if isinstance(field.field[self.pos[1]][self.pos[0]], Teleport):
            if self.dir == field.field[self.pos[1]][self.pos[0]].get_direction():
                self.rect.x = field.field[self.pos[1]][self.pos[0]].get_pair_teleport()[0] * pixel_tile
                self.rect.y = field.field[self.pos[1]][self.pos[0]].get_pair_teleport()[1] * pixel_tile

        if self.state == GhostState.is_stop:
            self.change_speed(field)
        elif self.state == GhostState.is_moving:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            self.pos[0] = round(self.rect[0] / pixel_tile)
            self.pos[1] = round(self.rect[1] / pixel_tile)
            if self.rect.x % pixel_tile == 0 and self.rect.y % pixel_tile == 0:
                self.state = GhostState.is_stop

    def reset_pos(self, pos):
        self.pos = pos
        self.rect.x = self.pos[0] * pixel_tile
        self.rect.y = self.pos[1] * pixel_tile

    def process_draw(self, screen: pygame.Surface):
        """Draw the Pacman into the screen"""
        if settings.is_in_haste:
            screen.blit(self.dead_image, self.rect)
        else:
            screen.blit(self.rot_image, self.rect)
