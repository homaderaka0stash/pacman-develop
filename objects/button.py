import pygame

from settings import MAIN_FONT, BLUE, ORANGE, MAROON, WHITE, YELLOW, GREEN, STYLES_FILE, FONT_SIZE


class ButtonObject:
    image = pygame.image.load("images/menu_button.png")

    def __init__(self, x, y, width, height, screen: pygame.Surface, text, text_size=FONT_SIZE, font=MAIN_FONT):
        self.screen = screen
        self.pos = [x, y]
        self.size = [width, height]
        self.color = None
        self.text_size = text_size
        self.text_color = None
        self.text = text
        self.font = font

    def button_customize(self):
        with open(STYLES_FILE, 'r') as f:
            if f.read().strip() == 'STYLE_1':
                self.color = ORANGE
                self.text_color = MAROON
        with open(STYLES_FILE, 'r') as f:
            if f.read().strip() == 'STYLE_2':
                self.color = BLUE
                self.text_color = YELLOW
        with open(STYLES_FILE, 'r') as f:
            if f.read().strip() == 'STYLE_3':
                self.color = GREEN
                self.text_color = WHITE

    def draw_button(self, screen):
        self.button_customize()
        screen.blit(self.image, (self.pos[0], self.pos[1]))
        font = pygame.font.Font(self.font, self.text_size)
        text = font.render(self.text, True, self.text_color)
        self.screen.blit(text, (self.pos[0] + (self.size[0] / 2 - text.get_width() / 2),
                                self.pos[1] + (self.size[1] / 2 - text.get_height() / 2)))

    def in_rect(self, pos):
        if self.pos[0] < pos[0] < self.pos[0] + self.size[0]:
            if self.pos[1] < pos[1] < self.pos[1] + self.size[1]:
                return True
        return False
