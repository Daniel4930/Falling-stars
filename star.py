import pygame, os

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.star_gravity = 3
        self.x = x
        self.y = y
        self.image = pygame.image.load(os.path.join("images", "star_image.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    # Allow the stars to fall down from the top of the screen
    def update(self):
        self.y += self.star_gravity
        self.rect.topleft = (self.x, self.y)