import pygame, os

'''
Initial_position info:
1 -> spawn from the top of the map
2 -> spawn from the right of the map
3 -> spawn from the left of the map
'''
class Star(pygame.sprite.Sprite):
    def __init__(self, x, y, initial_position, animated):
        super().__init__()
        self.star_speed = 3
        self.x = x
        self.y = y
        self.is_moving = True
        self.on_top_of_platform = False
        self.is_animated = animated
        self.initial_position = initial_position
        self.current_sprite = 0
        self.sprites = []
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_1.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_2.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_3.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_4.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_5.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_6.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_7.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_8.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_9.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_10.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_11.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_12.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_13.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_14.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_15.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_16.png")).convert_alpha())
        self.sprites.append(pygame.image.load(os.path.join("images/star", "star_image_17.png")).convert_alpha())

        self.image = pygame.image.load(os.path.join("images/star", "blue_star_image.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def platform_collision(self, platform_y):
        star_platform_collision_tolerance = self.star_speed + 2
        self.y = platform_y + star_platform_collision_tolerance
        self.on_top_of_platform = True

    def no_platform_collision(self):
        self.on_top_of_platform = False

    # Allow the stars to fall down from the top of the screen
    def update(self, level):
        if not self.on_top_of_platform and self.is_animated == False:
            self.y += self.star_speed

        if self.is_animated:
            self.image = self.sprites[int(self.current_sprite)]
            self.current_sprite += 0.50

            if level == 1:
                self.star_speed = 5
            elif level == 2:
                self.star_speed = 10
            elif level == 3:
                self.star_speed = 13

            if self.initial_position == 1:
                self.y += self.star_speed

            elif self.initial_position == 2:
                self.x -= self.star_speed

            elif self.initial_position == 3:
                self.x += self.star_speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

        self.rect.topleft = (self.x, self.y)
