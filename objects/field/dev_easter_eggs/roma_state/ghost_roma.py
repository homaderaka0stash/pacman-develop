import pygame
import random

from objects.field.dev_easter_eggs.roma_state.roma_state_settings import ghost_path
from objects.ghosts.ghost import Ghost
from objects.ghosts.ghost_state import GhostState
from settings import pixel_tile
from objects.field.teleport import Teleport
from objects.field.wall import Wall


random.seed(version=2)


class GhostRoma(Ghost):
    image: pygame.image = pygame.image.load(ghost_path)

    def __init__(self, field_width, start_position, way):
        super().__init__(field_width, start_position)
        self.Ghost_speed = 3
        self.way = way
        self.cur_dir = 0

    def change_speed(self, field):

        if self.state == GhostState.is_stop:
            pos0 = self.rect.x // pixel_tile
            pos1 = self.rect.y // pixel_tile

            self.dir = self.way[self.cur_dir]
            self.cur_dir = (self.cur_dir + 1) % len(self.way)

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

    def process_draw(self, screen: pygame.Surface):
        """Draw the Pacman into the screen"""
        screen.blit(self.rot_image, self.rect)
