import pygame, os, random
from star import Star

# Parent class
class Game():
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1000, 700
        self.STAR_SIZE, self.SLIME_HEIGHT, self.BORDER_THICKNESS, self.SLIME_WIDTH = 60, 100, 30, 130
        self.BORDER_LEFT_X, self.BORDER_LEFT_Y = 100, 0
        self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y = 870, 0
        self.SCORE_BOARD_WIDTH, self.SCORE_BOARD_HEIGHT = 80, 50
        self.RED = (255,0,0)
        self.DARK_RED = (144,1,57)
        self.BLACK = (0,0,0)
        self.alpha, self.score = 0, 0
        self.level = 1
        self.increase_difficulty = True
        self.game_state = "On home screen"

        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.BORDER_IMAGE = pygame.image.load(os.path.join("images", "wall_border.png")).convert_alpha()
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.png")).convert_alpha()
        self.MENU_IMAGE = pygame.image.load(os.path.join("images", "menu_image.png"))
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.FONT = pygame.font.SysFont('Arial',25)
        self.SCREEN_TRANSITION = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    # Check if mouse clicked on the button
    def mouse_clicked(self, button_x, button_y, button_width, button_height, button_text):
        mouse_pos = pygame.mouse.get_pos()
        if (button_x < mouse_pos[0] < button_x + button_width) and (button_y < mouse_pos[1] < button_y + button_height) and button_text == "START":
            self.game_state = "Exit home screen"
            return True
        return False
    
    def draw_starting_page(self, star_group, button_group, button_text, button_x, button_y):
        font_surface = self.FONT.render(button_text, True, self.BLACK)
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blit(self.MENU_IMAGE, (0,0))
        button_group.draw(self.WINDOW)
        self.WINDOW.blit(font_surface, (button_x + 15, button_y + 10))
        star_group.draw(self.WINDOW)
        button_group.update()
        star_group.update()
            
    # This method both empty all star sprites and creates screen transition when existing menu screen
    def exist_menu_screen(self, star_group):
        pygame.mouse.set_visible(False)
        star_group.empty()
        self.screen_transition()

    def screen_transition(self):
        # This while loop create screen transition when existing menu screen
        while self.alpha != 255:
            self.alpha += 3
            self.WINDOW.blit(self.MENU_IMAGE, (0,0))
            self.SCREEN_TRANSITION.set_alpha(self.alpha)
            self.WINDOW.blit(self.SCREEN_TRANSITION, (0,0))
            pygame.display.update()
        self.alpha = 0

    def current_level(self, platform_group, platform1, platform2, platform3, platform4, platform5):
        if self.level == 1 and self.increase_difficulty:
            platform_group.add(platform1)
            platform_group.add(platform2)
            platform_group.add(platform3)

        elif self.level == 2 and self.increase_difficulty:
            platform_group.add(platform4)

        elif self.level == 3 and self.increase_difficulty:
            platform_group.add(platform5)

        self.increase_difficulty = False

    def level_up(self):
        if self.score == 5 or self.score == 10:
            self.level += 1
            self.increase_difficulty = True

    # Spawn stars onto the map
    def spawn_star(self, star_group):
        star_group.add(Star(random.randrange(self.BORDER_LEFT_X + self.BORDER_THICKNESS, self.BORDER_RIGHT_X - self.STAR_SIZE), -(self.STAR_SIZE)))
    
    # Remove any star sprite/object that go outside the map 
    def remove_star_outside_map(self, star_group):
        list = star_group.sprites()
        for i in range(len(list)):
            if list[i].y > self.WINDOW_HEIGHT:
                star_group.remove(list[i])

    #Check if a star collide with a platform
    #If so, stop the star from falling down, and let the star stay on top of platform
    def star_and_platform_collision(self, platform_group, star_group):
        all_star = star_group.sprites()
        all_platform = platform_group.sprites()
        for i in range(len(all_star)):
            for y in range(len(all_platform)):
                if pygame.sprite.collide_rect(all_star[i], all_platform[y]):
                    all_star[i].platform_collision(all_platform[y].y - self.STAR_SIZE)

    # Check for star and slime collision
    def slime_and_stars_collision(self, slime, star_group):
        collided = slime.slime_star_collision(slime, star_group)
        self.score += len(collided)
        if collided:
            self.level_up()

    def draw(self, slime, star_group, slime_single_group, platform_group):
        font_surface = self.FONT.render("Score: " + str(self.score), True, self.RED)

        # Setup window's background, borders, and score board.
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blits([(self.BACKGROUND_IMAGE, (0,0)), 
                           (self.BORDER_IMAGE, (self.BORDER_LEFT_X, self.BORDER_LEFT_Y)), 
                           (self.BORDER_IMAGE, (self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y)),
                           (font_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0))])
        slime.input()
        slime_single_group.draw(self.WINDOW)
        platform_group.draw(self.WINDOW)
        star_group.draw(self.WINDOW)
        slime_single_group.update()
        platform_group.update()
        star_group.update()