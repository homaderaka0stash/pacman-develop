import pygame

import settings
from game import Game
from game_state import GameState
from objects.menu.main_menu import MainMenu
from objects.menu.pause_menu import PauseMenu

settings.state = GameState.main_menu


def main():
    pygame.init()
    while True:
        if settings.state == GameState.in_game:
            game = Game(settings.state)
            game.run()
        elif settings.state == GameState.pause:
            pause_menu = PauseMenu()
            pause_menu.main_loop()
        elif settings.state == GameState.main_menu:
            main_menu = MainMenu()
            main_menu.main_loop()
        elif settings.state == GameState.settings_menu:
            pass
        elif settings.state == GameState.highscores_menu:
            pass
        elif settings.state == GameState.game_over_screen:
            pass
        elif settings.state == GameState.roma:
            game = Game(settings.state)
            game.run()
        elif settings.state == GameState.ilya:
            pass


if __name__ == '__main__':
    main()
