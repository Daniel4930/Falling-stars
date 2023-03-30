import pygame
from game import Game

class Button(Game, pygame.sprite.Sprite):
    def __init__(self, text):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.width = 100
        self.height = 50
        self.x = (self.WINDOW_WIDTH / 2) - (self.width / 2)
        self.y = (self.WINDOW_HEIGHT / 2) - self.height
        self.text = text
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
