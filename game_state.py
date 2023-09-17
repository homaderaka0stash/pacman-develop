import enum


class GameState(enum.Enum):
    main_menu = 0
    settings_menu = 1
    highscores_menu = 2
    in_game = 3
    game_over_screen = 4
    pause = 5
    roma = "dead"
    ilya = "dead as roma"
