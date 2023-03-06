import pygame, os, random
from game import Game

class Star(Game, pygame.sprite.Sprite):
    def __init__(self):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.star_gravity = 3
        self.x = random.randrange(self.BORDER_LEFT_X + self.BORDER_THICKNESS, self.BORDER_RIGHT_X - self.STAR_SIZE)
        self.y = -(self.STAR_SIZE)
        self.image = pygame.image.load(os.path.join("images", "star_image.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    # Allow the stars to fall down from the top of the screen
    def update(self):
        self.y += self.star_gravity
        self.rect.topleft = (self.x, self.y)