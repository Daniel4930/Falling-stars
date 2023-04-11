import pygame, os

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.height = 40
        self.width = 230
        self.image = pygame.image.load(os.path.join("images", "platform.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.is_stationary = True
        self.rect.topleft = [self.x, self.y]