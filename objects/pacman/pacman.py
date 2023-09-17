import pygame
from pygame.rect import Rect
from pygame.surface import Surface

import settings
from settings import pixel_tile
from save_settings import Save
from main_settings import save_map_path, score_img_path
from game_state import GameState

from animation import Animation

from objects.field.collectible.collectible import Collectible
from objects.field.collectible.food import Food
from objects.field.collectible.bonus import Bonus
from objects.field.teleport import Teleport
from objects.field.wall import Wall
from objects.pacman.pacman_state import PacmanState
from objects.pacman.lives import Lives
from objects.score.score import Score
from objects.score.highscore_recorder import HighscoreRecorder

from objects.field.dev_easter_eggs.roma_state.collectible.chest import Chest
from objects.field.dev_easter_eggs.roma_state.collectible.ice_cream import Ice_cream
from objects.field.dev_easter_eggs.roma_state.counter import Counter
from objects.field.dev_easter_eggs.roma_state.destructible_wall import Destructible_wall
from objects.field.dev_easter_eggs.roma_state.roma_state_settings import final_res_ice_cream, final_res_chest


def state_change(st: GameState):
    settings.state = st


class Pacman:
    def __init__(self, pacman_speed, field_width, field_height, start_pacman_position, image_paths, food=10):
        self.field_height = field_height
        self.animation: Animation = Animation([im for im in image_paths], 3)
        self.image = pygame.image.load(image_paths[0])
        self.field_width = field_width
        self.pacman_speed = pacman_speed
        self.pos = start_pacman_position
        if settings.state == GameState.roma:
            self.counter_ice_cream = Counter(final_res_ice_cream)
            self.counter_chest = Counter(final_res_chest)
            self.score_img = pygame.image.load(score_img_path)
            self.img_rect = self.image.get_rect()
            self.img_rect.x = 50
            self.img_rect.y = 650
        elif settings.state == GameState.in_game:
            self.counter_food = Counter(food)
        self.state = PacmanState.is_stop
        self.dir = "no"
        self.intended_dir = "no"
        self.rot_image: pygame.image = None
        self.rect: Rect = self.image.get_rect()
        self.rect.x = self.pos[0] * pixel_tile
        self.rect.y = self.pos[1] * pixel_tile
        self.speed = [0, 0]
        self.lives = Lives(3)
        self.score = Score()

    def process_input(self, direction: str):
        self.intended_dir = direction

    def change_speed(self, field):
        # print(self.pos[0], self.pos[1])
        if self.state == PacmanState.is_stop:
            pos0 = self.rect.x // pixel_tile
            pos1 = self.rect.y // pixel_tile
            if self.intended_dir == "up":
                if not isinstance(field.field[pos1 - 1][pos0], Wall):
                    if isinstance(field.field[pos1 - 1][pos0], Destructible_wall):
                        if field.field[pos1 - 1][pos0].state:
                            self.dir = "up"
                    else:
                        self.dir = "up"

            elif self.intended_dir == "down":
                if not isinstance(field.field[pos1 + 1][pos0], Wall):
                    if isinstance(field.field[pos1 + 1][pos0], Destructible_wall):
                        if field.field[pos1 + 1][pos0].state:
                            self.dir = "down"
                    else:
                        self.dir = "down"

            elif self.intended_dir == "left":
                if not isinstance(field.field[pos1][pos0 - 1], Wall):
                    if isinstance(field.field[pos1][pos0 - 1], Destructible_wall):
                        # print('gg1')
                        # print(field.field[pos1][pos0 - 1].state)
                        # print(self.counter_ice_cream.cnt)
                        if field.field[pos1][pos0 - 1].state:
                            self.dir = "left"
                            # print('gg2')
                    else:
                        self.dir = "left"

            elif self.intended_dir == "right":
                if not isinstance(field.field[pos1][pos0 + 1], Wall):
                    if isinstance(field.field[pos1][pos0 + 1], Destructible_wall):
                        if field.field[pos1][pos0 + 1].state:
                            self.dir = "right"
                    else:
                        self.dir = "right"

            self.state = PacmanState.is_moving

            if self.dir == "up":
                if not isinstance(field.field[pos1 - 1][pos0], Wall):
                    if isinstance(field.field[pos1 - 1][pos0], Destructible_wall):
                        if field.field[pos1 - 1][pos0].state:
                            self.speed = [0, -self.pacman_speed]
                        else:
                            self.state = PacmanState.is_stop
                            self.dir = "no"
                            self.speed = [0, 0]
                    else:
                        self.speed = [0, -self.pacman_speed]
                else:
                    self.state = PacmanState.is_stop
                    self.dir = "no"
                    self.speed = [0, 0]

            elif self.dir == "down":
                if not isinstance(field.field[pos1 + 1][pos0], Wall):
                    if isinstance(field.field[pos1 + 1][pos0], Destructible_wall):
                        if field.field[pos1 + 1][pos0].state:
                            self.speed = [0, self.pacman_speed]
                        else:
                            self.state = PacmanState.is_stop
                            self.dir = "no"
                            self.speed = [0, 0]
                    else:
                        self.speed = [0, self.pacman_speed]
                else:
                    self.state = PacmanState.is_stop
                    self.dir = "no"
                    self.speed = [0, 0]

            elif self.dir == "left":
                if not isinstance(field.field[pos1][pos0 - 1], Wall):
                    if isinstance(field.field[pos1][pos0 - 1], Destructible_wall):
                        if field.field[pos1][pos0 - 1].state:
                            self.speed = [-self.pacman_speed, 0]
                        else:
                            self.state = PacmanState.is_stop
                            self.dir = "no"
                            self.speed = [0, 0]
                    else:
                        self.speed = [-self.pacman_speed, 0]
                else:
                    self.state = PacmanState.is_stop
                    self.dir = "no"
                    self.speed = [0, 0]

            elif self.dir == "right":
                if not isinstance(field.field[pos1][pos0 + 1], Wall):
                    if isinstance(field.field[pos1][pos0 + 1], Destructible_wall):
                        if field.field[pos1][pos0 + 1].state:
                            self.speed = [self.pacman_speed, 0]
                        else:
                            self.state = PacmanState.is_stop
                            self.dir = "no"
                            self.speed = [0, 0]
                    else:
                        self.speed = [self.pacman_speed, 0]
                else:
                    self.state = PacmanState.is_stop
                    self.dir = "no"
                    self.speed = [0, 0]

            elif self.dir == "no":
                self.state = PacmanState.is_stop
                self.speed = [0, 0]
            self.intended_dir = "no"

    def process_logic(self, field):
        if settings.state == GameState.roma and self.pos[0] == 31 and self.pos[1] == 29:
            state_change(GameState.main_menu)
        """Process game logic of the Pacman"""
        if isinstance(field.field[self.pos[1]][self.pos[0]], Teleport):
            if self.dir == field.field[self.pos[1]][self.pos[0]].get_direction():
                self.rect.x = field.field[self.pos[1]][self.pos[0]].get_pair_teleport()[0] * pixel_tile
                self.rect.y = field.field[self.pos[1]][self.pos[0]].get_pair_teleport()[1] * pixel_tile
            if self.intended_dir == "up":
                state_change(GameState.roma)
            elif self.intended_dir == "down":
                state_change(GameState.roma)

        if self.state == PacmanState.is_stop:
            self.change_speed(field)
        elif self.state == PacmanState.is_moving:
            self.rect.x += self.speed[0]
            self.rect.y += self.speed[1]
            self.pos[0] = round(self.rect[0] / pixel_tile)
            self.pos[1] = round(self.rect[1] / pixel_tile)

            if self.rect.x % pixel_tile == 0 and self.rect.y % pixel_tile == 0:
                self.state = PacmanState.is_stop

            if settings.state == GameState.roma:

                if isinstance(field.field[self.pos[1]][self.pos[0]], Ice_cream):
                    self.counter_ice_cream.cnt_upgrade()
                    for i in range(self.field_height):
                        for j in range(self.field_width):
                            if isinstance(field.field[i][j], Destructible_wall):
                                if field.field[i][j].type == 2:
                                    field.field[i][j].image_update(self.counter_ice_cream.check_cnt())
                            elif isinstance(field.field[i][j], Chest):
                                field.field[i][j].image_update(self.counter_ice_cream.check_cnt())
                    print(self.counter_ice_cream.cnt)

                if isinstance(field.field[self.pos[1]][self.pos[0]], Chest):
                    self.counter_chest.cnt_upgrade()
                    for i in range(self.field_height):
                        for j in range(self.field_width):
                            if isinstance(field.field[i][j], Destructible_wall):
                                if field.field[i][j].type == 1:
                                    field.field[i][j].image_update(self.counter_chest.check_cnt())
                    print(self.counter_chest.cnt)

                if isinstance(field.field[self.pos[1]][self.pos[0]], Destructible_wall):
                    field.field[self.pos[1]][self.pos[0]].process_collection(field.field)

            if isinstance(field.field[self.pos[1]][self.pos[0]], Collectible):
                if isinstance(field.field[self.pos[1]][self.pos[0]], Bonus):
                    settings.is_in_haste = True
                    settings.haste_beg_time = pygame.time.get_ticks()
                if isinstance(field.field[self.pos[1]][self.pos[0]], Food):
                    self.counter_food.cnt_upgrade()
                    self.score.update(10)
                    print(self.counter_food.cnt)
                    if self.counter_food.check_cnt():
                        state_change(GameState.main_menu)
                        hr = HighscoreRecorder()
                        hr.load()
                        hr.update(self.score.count)
                        hr.save()
                        Save(save_map_path, None, None, None, None, None, None, None).delete_save_map()
                field.field[self.pos[1]][self.pos[0]].process_collection(field.field)

    def reset_pos(self, pos):
        self.pos = pos
        self.state = PacmanState.is_stop
        self.rect.x = self.pos[0] * pixel_tile
        self.rect.y = self.pos[1] * pixel_tile

    def process_draw(self, screen: Surface):
        """Draw the Pacman into the screen"""
        self.image = self.animation.get_next_frame()
        if self.dir == "up":
            self.rot_image = pygame.transform.rotate(self.image, 90)
        elif self.dir == "down":
            self.rot_image = pygame.transform.rotate(self.image, -90)
        elif self.dir == "left":
            self.rot_image = pygame.transform.rotate(self.image, 180)
        elif self.dir == "right":
            self.rot_image = pygame.transform.rotate(self.image, 0)
        if self.dir == "no":
            if settings.state == GameState.in_game:
                self.rot_image = pygame.image.load("images/pacman1.png")
            elif settings.state == GameState.roma:
                self.rot_image = pygame.image.load("images/roma_state/pacman.png")

        screen.blit(self.rot_image, self.rect)
        if settings.state == GameState.in_game:
            self.lives.process_draw(screen)
            self.score.process_draw(screen)
        elif settings.state == GameState.roma:
            screen.blit(self.score_img, (self.img_rect.x, self.img_rect.y + 5))
            screen.blit(pygame.font.Font(settings.MAIN_FONT, 30).render(str(self.counter_ice_cream.cnt), True, pygame.Color('#FF7799')),
                        (self.img_rect.x + 20, self.img_rect.y))
            screen.blit(pygame.font.Font(settings.MAIN_FONT, 30).render(str(self.counter_chest.cnt), True, pygame.Color('#FF7799')),
                        (self.img_rect.x + 90, self.img_rect.y))
            screen.blit(pygame.image.load("images/roma_state/pacman1.png"), (450, 660))
