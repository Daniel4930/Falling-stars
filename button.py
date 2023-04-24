import pygame
from game import Game

class Button(Game, pygame.sprite.Sprite):
    def __init__(self, text, width, height, button_x, button_y):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.x = button_x
        self.y = button_y
        self.text = text
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
