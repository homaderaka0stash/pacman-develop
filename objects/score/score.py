import pygame
from main_settings import score_img_path
from settings import MAIN_FONT


class Score:
    def __init__(self):
        self.count = 0
        self.image = pygame.image.load(score_img_path)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 650
        self.score_font = pygame.font.Font(MAIN_FONT, 30)

    def update(self, n):
        self.count += n

    def process_draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color('#000000'), (self.rect.x, self.rect.y, self.rect.width + 100, self.rect.height + 30))
        screen.blit(self.score_font.render("Score: " + str(self.count), True, pygame.Color('#FF7799')), (self.rect.x + 30, self.rect.y + 5))
