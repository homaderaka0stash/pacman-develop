import pygame

from objects.field.collectible.collectible import Collectible


class Food(Collectible):
    filename = 'images/food.png'
    image = pygame.image.load(filename)
