import pygame

import settings
from game_state import GameState
from objects.button import ButtonObject
from settings import BLACK
from main_settings import width, height, size
from exit_game import exit_game

screen = pygame.display.set_mode(size)


class PauseMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        # Buttons
        self.resume_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 200, 250, 75,
                                          screen, text="RESUME")
        self.main_menu_button = ButtonObject((width // 2) - (250 // 2), height // 2 - 100, 250, 75,
                                             screen, text="MAIN MENU", text_size=33)
        self.exit_button = ButtonObject((width // 2) - (250 // 2), height // 2, 250, 75,
                                        screen, text="EXIT")
        self.in_pause = True
        self.exit = False
        # self.main_loop()

    def button_commands(self, pos):
        if self.resume_button.in_rect(pos):
            self.resume()
        if self.main_menu_button.in_rect(pos):
            self.main_menu()
        if self.exit_button.in_rect(pos):
            exit_game()

    def resume(self):
        self.in_pause = False
        settings.state = GameState.in_game

    def main_menu(self):
        self.in_pause = False
        settings.state = GameState.main_menu

    def render(self):
        self.screen.fill(BLACK)
        self.resume_button.draw_button(screen)
        self.main_menu_button.draw_button(screen)
        self.exit_button.draw_button(screen)

    def main_loop(self):
        while self.in_pause:

            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_commands(pos)
                if event.type == pygame.QUIT:
                    exit_game()

            self.render()
            pygame.display.flip()
            pygame.time.wait(15)
