import pygame

import settings
from game_state import GameState
from objects.button import ButtonObject
from main_settings import width, height, size
from exit_game import exit_game
from settings import STYLES_FILE

screen = pygame.display.set_mode(size)


class SettingsMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        # Buttons
        self.style_1_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 200, 250, 75,
                                           screen, text="STYLE 1")
        self.style_2_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 100, 250, 75,
                                           screen, text="STYLE 2")
        self.style_3_button = ButtonObject((width // 2) - (250 // 2), height // 2, 250, 75,
                                           screen, text="STYLE 3")
        self.back_button = ButtonObject((width // 2) - (250 // 2), height // 2 + 100, 250, 75,
                                        screen,  text="BACK")
        self.in_settings = True
        self.main_loop()

    def render(self):
        self.style_1_button.draw_button(self.screen)
        self.style_2_button.draw_button(self.screen)
        self.style_3_button.draw_button(self.screen)
        self.back_button.draw_button(self.screen)

    def button_commands(self, pos):
        if self.style_1_button.in_rect(pos):
            with open(STYLES_FILE, 'w') as f:
                f.write("STYLE_1")
        if self.style_2_button.in_rect(pos):
            with open(STYLES_FILE, 'w') as f:
                f.write("STYLE_2")
        if self.style_3_button.in_rect(pos):
            with open(STYLES_FILE, 'w') as f:
                f.write("STYLE_3")
        if self.back_button.in_rect(pos):
            self.in_settings = False
            settings.state = GameState.main_menu

    def main_loop(self):
        while self.in_settings:

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_commands(pos)
                if event.type == pygame.QUIT:
                    exit_game()
            self.render()
            pygame.display.flip()
            pygame.time.wait(15)
