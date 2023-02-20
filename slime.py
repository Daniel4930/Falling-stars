import pygame, os, sys
from game import Game

class Slime(Game, pygame.sprite.Sprite):
    def __init__(self, x, y, left_move):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.slime_speed = 5
        self.height = 20
        self.jumping = False
        self.velocity = self.height
        self.gravity = 1
        self.left_move = left_move
        if self.left_move == True:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "character_left_image.png")).convert_alpha(),(self.SLIME_SIZE, self.SLIME_SIZE))
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "character_right_image.png")).convert_alpha(),(self.SLIME_SIZE, self.SLIME_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    # Check for collision between a star and slime, only the star got deleted from the screen when collided
    def collision(self, slime, star_group):
        collided = pygame.sprite.spritecollide(slime, star_group, True, pygame.sprite.collide_circle_ratio(0.50))
        return collided

    def update(self):
        # Control the slime's movement using keyboard
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]: # move left
            self.x -= self.slime_speed
            self.left_move = True

        if key_pressed[pygame.K_RIGHT]: # move right
            self.x += self.slime_speed
            self.left_move = False

        if key_pressed[pygame.K_UP]:
            self.jumping = True
        # Logic part on how jumping work
        if self.jumping:
            self.y -= self.velocity
            self.velocity -= self.gravity
            if self.velocity < -self.height:
                self.jumping = False
                self.velocity = self.height

        if key_pressed[pygame.K_SPACE]:
            sys.exit()

        # This doesn't allow the slime to go over the borders and the map
        if self.x < self.BORDER_LEFT_X + self.BORDER_THICKNESS + self.slime_speed:
            self.x = self.BORDER_LEFT_X + self.BORDER_THICKNESS + self.slime_speed
        if self.x > self.BORDER_RIGHT_X - self.SLIME_SIZE - self.slime_speed:
            self.x = self.BORDER_RIGHT_X - self.SLIME_SIZE - self.slime_speed
        if self.y > self.WINDOW_HEIGHT - self.SLIME_SIZE:
            self.y = self.WINDOW_HEIGHT - self.SLIME_SIZE
        if self.y < 0:
            self.y = 0

        self.rect.topleft = [self.x, self.y]

        if self.left_move == False:
            # When slime moved right, display slime's image where it facing to the right
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "character_right_image.png")).convert_alpha(),(self.SLIME_SIZE, self.SLIME_SIZE))
        else:
            # When slime moved left, display slime's image where it facing to the left
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "character_left_image.png")).convert_alpha(),(self.SLIME_SIZE, self.SLIME_SIZE))