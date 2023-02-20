import pygame, os
from game import Game

class Star(Game, pygame.sprite.Sprite):
    def __init__(self, x, y):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.star_gravity = 2
        self.x, self.y = x, y
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "star_image.png")).convert_alpha(),(self.STAR_SIZE,self.STAR_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    # Allow the stars to fall down from the top of the screen
    def update(self):
        self.y += self.star_gravity
        self.rect.topleft = [self.x, self.y]
