import pygame, os

# Parent class
class Game:
    def __init__(self):
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1000, 700
        self.STAR_SIZE, self.SLIME_SIZE, self.BORDER_THICKNESS = 60, 100, 30
        self.BORDER_LEFT_X, self.BORDER_LEFT_Y = 100, 0
        self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y = 870, 0
        self.SCORE_BOARD_WIDTH, self.SCORE_BOARD_HEIGHT = 80, 50
        self.RED = (255,0,0)

        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.BORDER_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images", "wall_border.png")).convert_alpha(), (self.BORDER_THICKNESS, self.WINDOW_HEIGHT))
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.png")).convert_alpha()
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.FONT = pygame.font.SysFont('Arial',25)

    def draw(self, point):
        font_surface = self.FONT.render("Score: " + str(point), False, self.RED)

        # Setup window's background, borders, and score board.
        self.WINDOW.blits([(self.BACKGROUND_IMAGE, (0,0)), (self.BORDER_IMAGE, (self.BORDER_LEFT_X, self.BORDER_LEFT_Y)), (self.BORDER_IMAGE, (self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y)),(font_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0))])