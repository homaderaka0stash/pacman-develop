import pygame


class Lives:
    def __init__(self, a):
        self.lives_left = a
        self.image = pygame.image.load("images/pacman3.png")
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 660

    def decrease(self):
        self.lives_left = self.lives_left - 1

    def is_dead(self):
        if self.lives_left <= 0:
            return True
        return False

    def process_draw(self, screen: pygame.Surface):
        for i in range(3):
            pygame.draw.rect(screen, pygame.Color('#000000'), (self.rect.x + 30 * i, self.rect.y, self.rect.width, self.rect.height))
        for i in range(self.lives_left):
            screen.blit(self.image, (self.rect.x + 30 * i, self.rect.y))
