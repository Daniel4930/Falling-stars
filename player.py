import pygame, os
from game import Game

class Player(Game, pygame.sprite.Sprite):
    def __init__(self):
        Game.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.x = self.BORDER_LEFT_X + self.BORDER_THICKNESS
        self.y = self.WINDOW_HEIGHT - self.SLIME_HEIGHT
        self.health = 5
        self.is_falling = False
        self.is_on_ground = True
        self.jumping = False
        self.left_move = False
        self.is_animated = False
        self.slime_speed = 5
        self.tolerance = 15
        self.height, self.gravity, self.counter = 16, 1, 0
        self.velocity = self.height
        self.left_side_image = pygame.image.load(os.path.join("images", "character_left_image(original).png")).convert_alpha()
        self.right_side_image = pygame.image.load(os.path.join("images", "character_right_image(original).png")).convert_alpha()
        self.image = self.left_side_image
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def return_to_spawn_point(self):
        self.x = self.BORDER_LEFT_X + self.BORDER_THICKNESS
        self.y = self.WINDOW_HEIGHT - self.SLIME_HEIGHT

    def slime_on_ground(self):
        if self.y == self.WINDOW_HEIGHT - self.SLIME_HEIGHT:
            self.is_on_ground = True
            return
        self.is_on_ground = False
        self.is_falling = True

    def slime_star_collision(self, slime, star_group):
        star_collided = pygame.sprite.spritecollide(slime, star_group, True, pygame.sprite.collide_circle_ratio(0.50))
        return star_collided
    
    def collision_platform(self, slime, platform_group):
        all_platform = platform_group.sprites()
        collision_tolerance = 1
        for i in range(len(all_platform)):
            if pygame.sprite.collide_rect(slime, all_platform[i]):
                self.is_falling = False
                if all_platform[i].is_platform_vertical() == False:
                    if self.y >= all_platform[i].y:
                        self.y = all_platform[i].y + all_platform[i].height

                    if self.y + self.SLIME_HEIGHT <= all_platform[i].y + all_platform[i].height:
                        self.y = all_platform[i].y - self.SLIME_HEIGHT + collision_tolerance

                    elif self.x + self.tolerance > all_platform[i].x + all_platform[i].width:
                        self.x = all_platform[i].x + all_platform[i].width + 1

                    elif self.x + self.tolerance < all_platform[i].x:
                        self.x = all_platform[i].x - self.SLIME_WIDTH

                else: #Different method of checking collision between 
                      #slime and platform if platform is vertical (Vertical platform is introdude in level 3)

                    if self.x + self.tolerance > all_platform[i].x + all_platform[i].width:
                        self.x = all_platform[i].x + all_platform[i].width + 1
                    
                    elif self.y + self.SLIME_HEIGHT >= all_platform[i].y:
                        self.y = all_platform[i].y - self.SLIME_HEIGHT + collision_tolerance

    def free_fall(self):
        free_fall_speed = self.height - 5
        if self.jumping == False:
            self.y += free_fall_speed

    def input(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_LEFT]:
            self.x -= self.slime_speed
            self.left_move = True

        if key_pressed[pygame.K_RIGHT]:
            self.x += self.slime_speed
            self.left_move = False

        if key_pressed[pygame.K_UP] and (self.is_falling == False or self.is_on_ground):
            self.jumping = True
        if self.jumping:
            self.y -= self.velocity
            self.velocity -= self.gravity
            if self.velocity < -self.height:
                self.jumping = False
                self.velocity = self.height

        if self.x <= self.BORDER_LEFT_X + self.BORDER_THICKNESS + self.slime_speed:
            self.x = self.BORDER_LEFT_X + self.BORDER_THICKNESS + self.slime_speed
        if self.x >= self.BORDER_RIGHT_X - self.BORDER_THICKNESS - self.SLIME_HEIGHT - self.slime_speed:
            self.x = self.BORDER_RIGHT_X - self.SLIME_HEIGHT - self.BORDER_THICKNESS - self.slime_speed
        if self.y > self.WINDOW_HEIGHT - self.SLIME_HEIGHT:
            self.y = self.WINDOW_HEIGHT - self.SLIME_HEIGHT
        if self.y < 0:
            self.y = 0

    def slime_taken_damaged(self):
        if self.counter != 20:
            if self.counter % 2 == 0:
                self.alpha = 50
                self.right_side_image.set_alpha(self.alpha)
                self.left_side_image.set_alpha(self.alpha)
                self.counter += 1
            else:
                self.alpha = 255
                self.right_side_image.set_alpha(self.alpha)
                self.left_side_image.set_alpha(self.alpha)
                self.counter += 1
        else:
            self.alpha = 255
            self.counter = 0
            self.right_side_image.set_alpha(self.alpha)
            self.left_side_image.set_alpha(self.alpha)
            self.is_animated = False
    
    def update(self):
        if self.is_animated:
            self.slime_taken_damaged()

        if self.left_move == False:
            self.image = self.right_side_image
        else:
            self.image = self.left_side_image

        self.rect.topleft = [self.x, self.y]