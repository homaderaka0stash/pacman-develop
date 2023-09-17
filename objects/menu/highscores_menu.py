import pygame
import settings

from game_state import GameState
from main_settings import width, height, size
from settings import BLACK, YELLOW, MAIN_FONT
from exit_game import exit_game
from objects.button import ButtonObject
from objects.score.highscore_recorder import HighscoreRecorder

screen = pygame.display.set_mode(size)


class HighscoresMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        self.back_button = ButtonObject((width // 2) - (250 // 2), height // 2 + 200, 250, 75,
                                        screen, text="BACK")
        self.main_name_font = pygame.font.Font(MAIN_FONT, 90)
        self.scores = pygame.font.Font(MAIN_FONT, 50)
        self.text = None
        self.in_highscore = True
        self.get_scores()
        self.print_all_text()
        self.main_loop()

    def render(self):
        self.back_button.draw_button(screen)

    def button_commands(self, pos):
        if self.back_button.in_rect(pos):
            self.screen.fill(BLACK)
            self.in_highscore = False
            settings.state = GameState.main_menu

    def get_scores(self):
        try:
            f = open('objects/score/highscores.txt', 'r')
            self.text = list(f.read().split())
            f.close()
        except:
            self.text = ["0", "0", "0", "0", "0"]
            f = open('objects/score/highscores.txt', 'w')
            for i in self.text:
                f.write(i + ' ')
            f.close()

    def print_heading(self):
        level_heading = self.main_name_font.render('HIGHSCORES', True, YELLOW)
        screen.blit(level_heading, (0 + (size[0] / 2 - level_heading.get_width() / 2),
                                   (size[1] / 2 - level_heading.get_width() / 2)))

    def print_all_text(self):
        i = 1
        delimiter = 0
        self.print_heading()
        while i <= len(self.text):
            text_surface = self.scores.render('{}) - {}'.format(i, self.text[len(self.text) - i]), True, YELLOW)
            screen.blit(text_surface, (0 + (size[0] / 2 - text_surface.get_width() / 2),
                                       150 + delimiter))
            delimiter += 60
            i += 1

    def main_loop(self):
        while self.in_highscore:
            self.render()
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_commands(pos)
                if event.type == pygame.QUIT:
                    exit_game()
            pygame.display.flip()
            pygame.time.wait(15)
