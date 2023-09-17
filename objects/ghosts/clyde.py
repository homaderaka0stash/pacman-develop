import pygame
import random

from objects.field.teleport import Teleport
from objects.field.wall import Wall
from search.get_way import GetWay

from settings import pixel_tile
from objects.ghosts.ghost import Ghost
from objects.ghosts.ghost_state import GhostState

random.seed(version=2)


class Clyde(Ghost):
    filename = 'images/clyde.png'
    image: pygame.image = pygame.image.load(filename)

    def __init__(self, field_width, start_clyde_position):
        super().__init__(field_width, start_clyde_position)
    def change_speed(self, field):

        if self.state == GhostState.is_stop:

            self.state = GhostState.is_moving
            self.way = GetWay(self.pos[0], self.pos[1], self.pacman_pos[0], self.pacman_pos[1]).get_way()

            if len(self.way) > 7:
                self.dir = self.way[0]
            else:
                available_dirs = []
                pos0 = self.rect.x // pixel_tile
                pos1 = self.rect.y // pixel_tile

                if not isinstance(field.field[pos1 - 1][pos0], Wall) and self.dir != "down":
                    available_dirs.append("up")
                if not isinstance(field.field[pos1 + 1][pos0], Wall) and self.dir != "up":
                    available_dirs.append("down")
                if not isinstance(field.field[pos1][pos0 - 1], Wall) and self.dir != "right":
                    available_dirs.append("left")
                if not isinstance(field.field[pos1][pos0 + 1], Wall) and self.dir != "left":
                    available_dirs.append("right")

                self.dir = random.choice(available_dirs)


            if self.dir == "up":
                self.speed = [0, -self.Ghost_speed]
                self.rot_image = pygame.transform.rotate(self.image, 0)
            elif self.dir == "down":
                self.speed = [0, self.Ghost_speed]
                self.rot_image = pygame.transform.rotate(self.image, 0)
            elif self.dir == "left":
                self.speed = [-self.Ghost_speed, 0]
                self.rot_image = pygame.transform.rotate(self.image, 0)
            elif self.dir == "right":
                self.speed = [self.Ghost_speed, 0]
                self.rot_image = pygame.transform.rotate(self.image, 0)
            elif self.dir == "no":
                self.state = GhostState.is_stop
                self.speed = [0, 0]

    def process_logic(self, field, pacman_pos):
        """Process game logic of the Blinky"""
        self.pacman_pos = pacman_pos
        self.pos[0] = self.rect.x // pixel_tile
        self.pos[1] = self.rect.y // pixel_tile

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

