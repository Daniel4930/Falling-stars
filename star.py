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

    #Create star in an interval (the interval is in main.py)
    def create_star(self, star_group):
        star_group.add(Star())

    #Remove any star sprite/object that go outside the map 
    def remove_star(self, star_group):
        list = star_group.sprites()
        for i in range(len(list)):
            if list[i].y > self.WINDOW_HEIGHT:
                star_group.remove(list[i])

    # Allow the stars to fall down from the top of the screen
    def update(self):
        self.y += self.star_gravity
        self.rect.topleft = (self.x, self.y)