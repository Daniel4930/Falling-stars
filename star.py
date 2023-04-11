import pygame, os

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.star_gravity = 3
        self.x = x
        self.y = y
        self.is_moving = True
        self.on_top_of_platform = False
        self.is_animated = False
        self.sprites = []
        self.current_sprite = 0
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

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def animated(self):
        self.is_animated = True
    
    def stop_animation(self):
        self.is_animated = False

    def platform_collision(self, platform_y):
        star_platform_collision_tolerance = 3
        self.y = platform_y + star_platform_collision_tolerance
        self.on_top_of_platform = True

    # Allow the stars to fall down from the top of the screen
    def update(self):
        if not self.on_top_of_platform:
            self.y += self.star_gravity
        self.rect.topleft = (self.x, self.y)
        if self.is_animated:
            self.current_sprite += 0.50

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.image = self.sprites[int(self.current_sprite)]
