import pygame

import settings

from game_state import GameState
from objects.button import ButtonObject
from main_settings import width, height, size
from exit_game import exit_game
from settings import YELLOW, MAIN_FONT, BLACK
from objects.menu.settings_menu import SettingsMenu
from objects.menu.highscores_menu import HighscoresMenu

screen = pygame.display.set_mode(size)


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        self.main_name_font = pygame.font.Font(MAIN_FONT, 100)
        # Buttons
        self.start_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 150, 250, 75,
                                         screen, text="PLAY")
        self.settings_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 50, 250, 75,
                                            screen, text="SETTINGS")
        self.highscore_button = ButtonObject((width // 2) - (250 // 2), height // 2 + 50, 250, 75,
                                             screen, text="HIGHSCORES", text_size=30)
        self.exit_button = ButtonObject((width // 2) - (250 // 2), height // 2 + 150, 250, 75,
                                        screen, text="EXIT")
        self.in_menu = True
        self.print_heading()

    # надо фиксить, тк работает ток когда в цикле
    def print_heading(self):
        level_heading = self.main_name_font.render('PACMAN', True, YELLOW)
        screen.blit(level_heading, (0 + (size[0] / 2 - level_heading.get_width() / 2),
                                    20))

    def render(self):
        self.start_button.draw_button(screen)
        self.settings_button.draw_button(screen)
        self.highscore_button.draw_button(screen)
        self.exit_button.draw_button(screen)

    def button_commands(self, pos):
        if self.start_button.in_rect(pos):
            self.start_game()
        if self.settings_button.in_rect(pos):
            self.in_menu = False
            SettingsMenu()
        if self.highscore_button.in_rect(pos):
            HighscoresMenu()
        if self.exit_button.in_rect(pos):
            exit_game()

    def start_game(self):
        settings.state = GameState.in_game
        self.in_menu = False

    def main_loop(self):
        while self.in_menu:
            self.print_heading()
            self.render()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_commands(pos)
                if event.type == pygame.QUIT:
                    exit_game()
            pygame.display.flip()
            pygame.time.wait(15)
