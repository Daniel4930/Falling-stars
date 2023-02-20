import pygame, os, random, sys
pygame.init()
pygame.display.init()

# Constant variables
RED = (255,0,0)
BACKGROUND_COLOR = (186,237,255)
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
STAR_SIZE, SLIME_SIZE, BORDER_THICKNESS = 60, 100, 30
BORDER_LEFT_X, BORDER_LEFT_Y = 100, 0
BORDER_RIGHT_X, BORDER_RIGHT_Y = 870, 0
SCORE_BOARD_WIDTH, SCORE_BOARD_HEIGHT = 80, 50

WINDOW = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
FONT = pygame.font.SysFont('Arial',25)
GAME_TITILE = pygame.display.set_caption("Falling Stars")

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y, left_move):
        super().__init__()
        self.x = x
        self.y = y
        self.height = 20
        self.jumping = False
        self.velocity = self.height
        self.gravity = 1
        self.left_move = left_move
        if self.left_move == True:
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("character_left_image.png")).convert_alpha(),(SLIME_SIZE, SLIME_SIZE))
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("character_right_image.png")).convert_alpha(),(SLIME_SIZE, SLIME_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    # Check for collision between a star and slime, only the star got deleted from the screen when collided
    def collision(self, slime, star_group):
        collided = pygame.sprite.spritecollide(slime, star_group, True, pygame.sprite.collide_circle_ratio(0.50))
        return collided

    def update(self, slime_movement_speed):
        # Control the slime's movement using keyboard
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self.jumping = True
        
        # Logic part on how jumping work
        if self.jumping:
            self.y -= self.velocity
            self.velocity -= self.gravity
            if self.velocity < -self.height:
                self.jumping = False
                self.velocity = self.height

        if key_pressed[pygame.K_LEFT]: # move left
            self.x -= slime_movement_speed
            self.left_move = True

        if key_pressed[pygame.K_RIGHT]: # move right
            self.x += slime_movement_speed
            self.left_move = False

        self.rect.topleft = [self.x, self.y]

        if self.left_move == False:
            # When slime moved right, display slime's image where it facing to the right
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("character_right_image.png")).convert_alpha(),(SLIME_SIZE, SLIME_SIZE))
        else:
            # When slime moved left, display slime's image where it facing to the left
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("character_left_image.png")).convert_alpha(),(SLIME_SIZE, SLIME_SIZE))

class Star(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.STAR_SIZE = 60
        self.x, self.y = x, y
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("star_image.png")).convert_alpha(),(self.STAR_SIZE,self.STAR_SIZE))
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    # Allow the stars to fall down from the top of the screen
    def update(self, star_falling_speed):
        self.y += star_falling_speed
        self.rect.topleft = [self.x, self.y]

def draw(point):
    BORDER_IMAGE = pygame.image.load(os.path.join("wall_border.png")).convert_alpha()
    font_surface = FONT.render("Score: " + str(point), False, RED)

    # Setup window's background, borders, and score board.
    WINDOW.fill(BACKGROUND_COLOR)
    WINDOW.blits([(BORDER_IMAGE, (BORDER_LEFT_X, BORDER_LEFT_Y)), (BORDER_IMAGE, (BORDER_RIGHT_X, BORDER_RIGHT_Y)),(font_surface, (BORDER_RIGHT_X + BORDER_THICKNESS, 0))])

def main():
    now = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps = 60
    score = 0
    left_move, run = True, True
    slime_movement_speed = 5
    star_movement_speed = 2

    slime = Slime((WINDOW_WIDTH/2) - (SLIME_SIZE/2), (WINDOW_HEIGHT - SLIME_SIZE), left_move)
    slime_group = pygame.sprite.Group()
    slime_group.add(slime)
    star_group = pygame.sprite.Group()
        
    while run:
        frame.tick(fps)
        for event in pygame.event.get():
            # To stop the game, click the red button on the window
            if event.type == pygame.QUIT:
                run = True
                sys.exit()

        # This doesn't allow the slime to go over the borders and the map
        if slime.x < BORDER_LEFT_X + BORDER_THICKNESS + slime_movement_speed:
            slime.x = BORDER_LEFT_X + BORDER_THICKNESS + slime_movement_speed
        if slime.x > BORDER_RIGHT_X - SLIME_SIZE - slime_movement_speed:
            slime.x = BORDER_RIGHT_X - SLIME_SIZE - slime_movement_speed
        if slime.y > WINDOW_HEIGHT - SLIME_SIZE:
            slime.y = WINDOW_HEIGHT - SLIME_SIZE
        if slime.y < 0:
            slime.y = 0

        # Create star sprites and store all sprites a group
        cooldown = pygame.time.get_ticks() - now
        if cooldown >= 3000:
            new_star = Star(random.randint(BORDER_LEFT_X + BORDER_THICKNESS, BORDER_RIGHT_X - STAR_SIZE), -(STAR_SIZE))
            star_group.add(new_star)
            now = pygame.time.get_ticks()

        # If collided, increase the score by 1
        collided_stars = slime.collision(slime, star_group)
        for num_star in collided_stars:
            score += 1
        
        # Display the game
        draw(score)
        slime_group.draw(WINDOW)
        slime_group.update(slime_movement_speed)
        star_group.draw(WINDOW)
        star_group.update(star_movement_speed)
        pygame.display.update()

if __name__ == "__main__":
    main()