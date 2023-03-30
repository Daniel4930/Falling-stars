import pygame, os, random
from star import Star

# Parent class
class Game():
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1000, 700
        self.STAR_SIZE, self.SLIME_SIZE, self.BORDER_THICKNESS = 60, 100, 30
        self.BORDER_LEFT_X, self.BORDER_LEFT_Y = 100, 0
        self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y = 870, 0
        self.SCORE_BOARD_WIDTH, self.SCORE_BOARD_HEIGHT = 80, 50
        self.RED = (255,0,0)
        self.DARK_RED = (144,1,57)
        self.BLACK = (0,0,0)
        self.alpha, self.score = 0, 0
        self.game_state = "On home screen"

        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.BORDER_IMAGE = pygame.image.load(os.path.join("images", "wall_border.png")).convert_alpha()
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.png")).convert_alpha()
        self.MENU_IMAGE = pygame.image.load(os.path.join("images", "menu_image.png"))
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.FONT = pygame.font.SysFont('Arial',25)
        self.SCREEN_TRANSITION = pygame.surface.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    #Check if mouse clicked on the button
    def mouse_clicked(self, button_x, button_y, button_width, button_height):
        mouse_pos = pygame.mouse.get_pos()
        if (button_x < mouse_pos[0] < button_x + button_width) and (button_y < mouse_pos[1] < button_y + button_height):
            self.game_state = "Exit home screen"
            return True
        return False
    
    def draw_starting_page(self, star_group, button_single_group, button_text, button_x, button_y):
        font_surface = self.FONT.render(button_text, True, self.BLACK)
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blit(self.MENU_IMAGE, (0,0))
        button_single_group.draw(self.WINDOW)
        self.WINDOW.blit(font_surface, (button_x + 15, button_y + 10))
        star_group.draw(self.WINDOW)
        button_single_group.update()
        star_group.update()
            
    #This method both empty all star sprites and creates screen transition when existing menu screen
    def exist_menu_screen(self, star_group):
        pygame.mouse.set_visible(False)
        star_group.empty()
        #This while loop create screen transition when existing menu screen
        while self.alpha != 255:
            self.alpha += 3
            self.WINDOW.blit(self.MENU_IMAGE, (0,0))
            self.SCREEN_TRANSITION.set_alpha(self.alpha)
            self.WINDOW.blit(self.SCREEN_TRANSITION, (0,0))
            pygame.display.update()
        self.alpha = 0

    #spawn stars onto the map
    def spawn_star(self, star_group):
        star_group.add(Star(random.randrange(self.BORDER_LEFT_X + self.BORDER_THICKNESS, self.BORDER_RIGHT_X - self.STAR_SIZE), -(self.STAR_SIZE)))
    
     #Remove any star sprite/object that go outside the map 
    def remove_star(self, star_group):
        list = star_group.sprites()
        for i in range(len(list)):
            if list[i].y > self.WINDOW_HEIGHT:
                star_group.remove(list[i])

    def slime_and_stars_collision(self, slime, star_group):
        collided = slime.collision(slime, star_group)
        self.score += len(collided)

    def draw(self, slime, star_group, slime_single_group):
        font_surface = self.FONT.render("Score: " + str(self.score), True, self.RED)
        # Setup window's background, borders, and score board.
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blits([(self.BACKGROUND_IMAGE, (0,0)), (self.BORDER_IMAGE, (self.BORDER_LEFT_X, self.BORDER_LEFT_Y)), (self.BORDER_IMAGE, (self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y)),(font_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0))])
        slime.input()
        slime_single_group.draw(self.WINDOW)
        star_group.draw(self.WINDOW)
        slime_single_group.update()
        star_group.update()