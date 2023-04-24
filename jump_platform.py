import pygame, os
from game import Game

class Platform(Game, pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Game.__init__(self)
        self.x = x
        self.y = y
        self.platform_speed = 1
        self.height = 40
        self.width = 230
        self.image = pygame.image.load(os.path.join("images", "platform.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.is_stationary = True
        self.is_moving_left = True
        self.is_vertical = False
        self.rect.topleft = [self.x, self.y]

    def border_collision(self):
        if self.x == self.BORDER_LEFT_X + self.BORDER_THICKNESS:
            self.is_moving_left = True
        elif self.x + self.width == self.BORDER_RIGHT_X:
            self.is_moving_left = False

    def rotate_platform(self):
        self.image = pygame.image.load(os.path.join("images", "vertical_platform.png")).convert_alpha()
        self.is_vertical = True
        self.image = pygame.transform.rotate(self.image, -90)
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        temp = self.height
        self.height = self.width
        self.width = temp

    def is_platform_vertical(self):
        return self.is_vertical

    def platform_moving(self):
        self.is_stationary = False

    def update(self):
        if self.is_stationary == False:
            if self.is_moving_left:
                self.x += self.platform_speed
            else:
                self.x -= self.platform_speed

        self.border_collision()
        self.rect.topleft = [self.x, self.y]