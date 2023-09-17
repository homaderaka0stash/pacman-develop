import os
import pygame

import settings
import main_settings as ms
from exit_game import exit_game
from game_state import GameState
from objects.field.field import Field
from objects.pacman.pacman import Pacman
from objects.ghosts.pinky import Pinky
from objects.ghosts.clyde import Clyde
from objects.ghosts.blinky import Blinky
from objects.ghosts.inky import Inky
from objects.field.dev_easter_eggs.roma_state.ghost_roma import GhostRoma
from main_settings import save_map_path, save_ghost_path
from save_settings import Save


class Game:
    def __init__(self, game_state):
        self.game_state = game_state
        self.game_over = False
        if settings.state == GameState.in_game:
            self.screen = pygame.display.set_mode(ms.size)
            self.blinky = Blinky(ms.field_width, ms.start_blinky_position)
            self.pinky = Pinky(ms.field_width, ms.start_pinky_position)
            self.inky = Inky(ms.field_width, ms.start_inky_position)
            self.clyde = Clyde(ms.field_width, ms.start_clyde_position)
            self.blinky.reset_pos([15, 11])
            self.pinky.reset_pos([16, 11])
            self.inky.reset_pos([14, 11])
            self.clyde.reset_pos([13, 11])
            self.blinky_delay = 0
            self.pinky_delay = 0
            self.inky_delay = 0
            self.clyde_delay = 0
            self.ghosts_eaten = 0
            if os.path.exists(save_map_path):
                self.field = Field(ms.save_map_path, ms.field_width, ms.field_height)
                with open(save_map_path, 'r') as f:
                    last_line = list(f.readlines()[-1].strip().split())
                    print(last_line)
                    self.pacman = Pacman(ms.pacman_speed, ms.field_width, ms.field_height,
                                         list((int(last_line[1]), int(last_line[2]))),
                                         ms.image_paths, self.field.food_count)
            else:
                self.field = Field(ms.map_path, ms.field_width, ms.field_height)
                self.pacman = Pacman(ms.pacman_speed, ms.field_width, ms.field_height, list(ms.start_pacman_position),
                                     ms.image_paths, self.field.food_count)
            if os.path.exists(save_ghost_path):
                with open(save_ghost_path, 'r') as f:
                    self.blinky.reset_pos(list(map(int, f.readline().split())))
                    self.pinky.reset_pos(list(map(int, f.readline().split())))
                    self.inky.reset_pos(list(map(int, f.readline().split())))
                    self.clyde.reset_pos(list(map(int, f.readline().split())))
            if os.path.exists(ms.save_score_path):
                with open(ms.save_score_path) as f:
                    self.pacman.score.count, self.pacman.lives.lives_left = map(int, f.readline().split())

        elif settings.state == GameState.roma:
            import objects.field.dev_easter_eggs.roma_state.roma_state_settings as rss
            self.screen = pygame.display.set_mode(rss.size)
            self.field = Field(rss.map_path, rss.field_width, rss.field_height)
            self.pacman = Pacman(rss.pacman_speed, rss.field_width, rss.field_height, list(rss.start_pacman_position),
                                 rss.image_paths)
            self.ghost_arr = [
                GhostRoma(rss.field_width, [14, 3], ["right", "right", "up", "up", "right", "right", "down", "down", "down", "down", "left", "right", "up", "up", "up", "up", "left", "left", "down", "down", "left", "left"]),
                GhostRoma(rss.field_width, [5, 5], ["right", "right", "right", "right", "down", "down", "down", "down", "left", "left", "up", "up", "left", "left", "up", "up"]),
                GhostRoma(rss.field_width, [20, 3], ["left", "down", "down", "right", "down", "down", "left", "left", "down", "down", "right", "right", "right", "right", "up", "right", "right", "right", "right", "up", "up", "up", "up", "up", "left", "left", "left", "right", "right", "right", "down", "down", "down", "down", "down", "left", "left", "left", "left", "down", "left", "left", "left", "left", "up", "up", "right", "right", "up", "up", "left", "up", "up", "right"]),
                GhostRoma(rss.field_width, [15, 17], ["right", "right", "right", "down", "down", "left", "left", "left", "up", "up"]),
                GhostRoma(rss.field_width, [3, 17], ["right", "right", "down", "down", "right", "right", "up", "right", "right", "down", "down", "down", "left", "left", "left", "left", "down", "left", "left", "up", "up", "up", "up", "up"]),
                GhostRoma(rss.field_width, [17, 21], ["left", "left", "down", "down", "right", "right", "right", "right", "up", "up", "down", "down", "left", "left", "left", "left", "up", "up" "right", "right"]),
                GhostRoma(rss.field_width, [26, 16], ["up", "right", "right", "up", "right", "right", "down", "down", "down", "down", "left", "left", "left", "right", "right", "right", "up", "up", "up", "up", "left", "left", "down", "left", "left", "down"]),
                GhostRoma(rss.field_width, [9, 27], ["left", "left", "left", "left", "up", "left", "left", "down", "down", "down", "right", "right", "right", "right", "right", "right", "right", "right", "up", "up", "down", "down", "left", "left", "left", "left", "left", "left", "left", "left", "up", "up", "up", "right", "right", "down", "right", "right", "right", "right", "right", "right", "right", "right"]),
                GhostRoma(rss.field_width, [23, 23], ["right", "up", "right", "right", "down", "down", "down", "down", "left", "left", "up", "left", "up", "up"])
            ]
            self.init_time = pygame.time.get_ticks()

    def run(self):
        while not self.game_over and settings.state == self.game_state:
            # Обработка событий
            # Проверка нажатия клавиш
            pressed = pygame.key.get_pressed()
            if pressed[97]:  # A
                self.pacman.process_input("left")
            elif pressed[119]:  # W
                self.pacman.process_input("up")
            elif pressed[100]:  # D
                self.pacman.process_input("right")
            elif pressed[115]:  # S
                self.pacman.process_input("down")
            # print("keys")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == 27:
                        self.game_over = True
                        break
                    if event.key == pygame.K_SPACE:
                        if settings.state == GameState.in_game:
                            Save(save_map_path, self.pacman.pos, self.blinky.pos, self.pinky.pos, self.inky.pos, self.clyde.pos, self.pacman.score.count, self.pacman.lives.lives_left).create_save_map(self.field.field)
                            settings.state = GameState.pause
            # print("events")
            # print(self.pacman.pos[0], self.pacman.pos[1])
            self.pacman.process_logic(self.field)

            if settings.state != self.game_state:
                break

            if settings.state == GameState.in_game:

                self.blinky.process_logic(self.field, self.pacman.pos)
                self.pinky.process_logic(self.field)
                self.inky.process_logic(self.field)
                self.clyde.process_logic(self.field, self.pacman.pos)

                if self.blinky_delay != 0:
                    if pygame.time.get_ticks() - self.blinky_delay < 5000:
                        self.blinky.reset_pos([15, 13])
                    else:
                        self.blinky_delay = 0
                if self.pinky_delay != 0:
                    if pygame.time.get_ticks() - self.pinky_delay < 5000:
                        self.pinky.reset_pos([16, 13])
                    else:
                        self.pinky_delay = 0
                if self.inky_delay != 0:
                    if pygame.time.get_ticks() - self.inky_delay < 5000:
                        self.inky.reset_pos([15, 14])
                    else:
                        self.inky_delay = 0
                if self.clyde_delay != 0:
                    if pygame.time.get_ticks() - self.clyde_delay < 5000:
                        self.clyde.reset_pos([16, 14])
                    else:
                        self.clyde_delay = 0

                if not settings.is_in_haste:
                    self.ghosts_eaten = 0

                if self.pacman.rect.colliderect(self.blinky.rect) or self.pacman.rect.colliderect(self.pinky.rect) or \
                    self.pacman.rect.colliderect(self.inky.rect) or self.pacman.rect.colliderect(self.clyde.rect):
                    if not settings.is_in_haste:
                        self.pacman.lives.decrease()
                        self.pacman.reset_pos([15, 23])
                        self.blinky.reset_pos([15, 11])
                        self.pinky.reset_pos([16, 11])
                        self.inky.reset_pos([14, 11])
                        self.clyde.reset_pos([13, 11])
                        pygame.time.wait(500)
                        if self.pacman.lives.is_dead():
                            self.game_over = True
                            settings.state = GameState.main_menu
                            Save(save_map_path, None, None, None, None, None, None, None).delete_save_map()
                    else:
                        if self.pacman.rect.colliderect(self.blinky.rect):
                            self.blinky.reset_pos([15, 11])
                            self.blinky_delay = pygame.time.get_ticks()
                        elif self.pacman.rect.colliderect(self.pinky.rect):
                            self.pinky.reset_pos([16, 11])
                            self.pinky_delay = pygame.time.get_ticks()
                        elif self.pacman.rect.colliderect(self.inky.rect):
                            self.inky.reset_pos([14, 11])
                            self.inky_delay = pygame.time.get_ticks()
                        elif self.pacman.rect.colliderect(self.clyde.rect):
                            self.clyde.reset_pos([13, 11])
                            self.clyde_delay = pygame.time.get_ticks()
                        self.ghosts_eaten += 1
                        self.pacman.score.update(200 * self.ghosts_eaten)
            else:
                if pygame.time.get_ticks() - self.init_time > 300000:
                    self.game_over = True
                    settings.state = GameState.main_menu
                    Save(save_map_path, None, None, None, None, None, None, None).delete_save_map()
                for ghost in self.ghost_arr:
                    ghost.process_logic(self.field)
                    if self.pacman.rect.colliderect(ghost.rect):
                        self.game_over = True
                        settings.state = GameState.main_menu
                        Save(save_map_path, None, None, None, None, None, None, None).delete_save_map()

            if pygame.time.get_ticks() - settings.haste_beg_time > 5000:
                settings.is_in_haste = False

            self.field.process_draw(self.screen)
            self.pacman.process_draw(self.screen)
            if settings.state == GameState.in_game:
                self.blinky.process_draw(self.screen)
                self.pinky.process_draw(self.screen)
                self.inky.process_draw(self.screen)
                self.clyde.process_draw(self.screen)
            elif settings.state == GameState.roma:
                for ghost in self.ghost_arr:
                    ghost.process_draw(self.screen)

            self.field.process_tele_draw(self.screen)

            # print("draw")
            pygame.display.flip()
            pygame.time.wait(15)
