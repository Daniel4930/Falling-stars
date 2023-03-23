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
        self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT = 100, 50
        self.MENU_BUTTON_X, self.MENU_BUTTON_Y = (self.WINDOW_WIDTH / 2) - (self.MENU_BUTTON_WIDTH / 2), (self.WINDOW_HEIGHT / 2) - self.MENU_BUTTON_HEIGHT
        self.RED = (255,0,0)
        self.DARK_RED = (144,1,57)
        self.BLACK = (0,0,0)
        self.button_pressed = False
        self.alpha, self.score = 0, 0

        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.BORDER_IMAGE = pygame.image.load(os.path.join("images", "wall_border.png")).convert_alpha()
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.png")).convert_alpha()
        self.MENU_IMAGE = pygame.image.load(os.path.join("images", "menu_image.png"))
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.FONT = pygame.font.SysFont('Arial',25)
        self.MENU_BUTTON = pygame.Rect(self.MENU_BUTTON_X, self.MENU_BUTTON_Y, self.MENU_BUTTON_WIDTH, self.MENU_BUTTON_HEIGHT)
        self.SCREEN_TRANSITION = pygame.surface.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.MENU_BUTTON_TEXT = self.FONT.render("START", False, (255,255,255))

    #Check if mouse clicked on the button
    def menu_screen(self, menu):
        mouse_pos = pygame.mouse.get_pos()
        if (self.MENU_BUTTON_X < mouse_pos[0] < self.MENU_BUTTON_X + self.MENU_BUTTON_WIDTH) and (self.MENU_BUTTON_Y < mouse_pos[1] < self.MENU_BUTTON_Y + self.MENU_BUTTON_HEIGHT):
            self.button_pressed = True
            return False
        else:
            if menu == True:
                return True
            else:
                return False
            
    #This method both empty all star sprites and creates screen transition when existing menu screen
    def exist_menu_screen(self, star_group):
        star_group.empty()
        #This while loop create screen transition when existing menu screen
        while self.alpha != 255:
            self.alpha += 3
            self.SCREEN_TRANSITION.set_alpha(self.alpha)
            self.draw_menu()
            self.WINDOW.blit(self.SCREEN_TRANSITION, (0,0))
            pygame.display.update()
        self.alpha = 0

    #spawn stars onto the map
    def spawn_star(self):
        return Star(random.randrange(self.BORDER_LEFT_X + self.BORDER_THICKNESS, self.BORDER_RIGHT_X - self.STAR_SIZE), -(self.STAR_SIZE))
    
     #Remove any star sprite/object that go outside the map 
    def remove_star(self, star_group):
        list = star_group.sprites()
        for i in range(len(list)):
            if list[i].y > self.WINDOW_HEIGHT:
                star_group.remove(list[i])

    def update_score(self, score):
        self.score = score

    def draw_menu(self):
        self.WINDOW.blit(self.MENU_IMAGE, (0,0))
        if self.button_pressed:
            pygame.draw.rect(self.WINDOW, self.DARK_RED, self.MENU_BUTTON)
        else:
            pygame.draw.rect(self.WINDOW, self.RED, self.MENU_BUTTON)
        self.WINDOW.blit(self.MENU_BUTTON_TEXT, (self.MENU_BUTTON_X + 10, self.MENU_BUTTON_Y + 10))

    def draw(self):
        font_surface = self.FONT.render("Score: " + str(self.score), False, self.RED)
        # Setup window's background, borders, and score board.
        self.WINDOW.blits([(self.BACKGROUND_IMAGE, (0,0)), (self.BORDER_IMAGE, (self.BORDER_LEFT_X, self.BORDER_LEFT_Y)), (self.BORDER_IMAGE, (self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y)),(font_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0))])