import pygame, os, random
pygame.init()
pygame.display.init()

# Constant variables
BROWN = (100,40,0)
RED = (255,0,0)
BACKGROUND_COLOR = (186,237,255)

class Map():
    def __init__(self):
        pygame.font.init()
        self.FONT = pygame.font.SysFont('Arial',25)
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1000, 700
        self.BORDER_THICKNESS = 30
        self.BORDER_LEFT_X, self.BORDER_LEFT_Y = 100, 0
        self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y = 870, 0
        self.SCORE_BOARD_WIDTH, self.SCORE_BOARD_HEIGHT = 80, 50
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.SCORE_BOARD = pygame.Rect(self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0, self.SCORE_BOARD_WIDTH, self.SCORE_BOARD_HEIGHT)
        self.BORDER_IMAGE = pygame.image.load(os.path.join("wall_border.png")).convert_alpha()
        self.points = 0

    def score(self,score):
        self.points = score

    def draw(self):
        self.WINDOW.fill(BACKGROUND_COLOR)
        self.WINDOW.blits([(self.BORDER_IMAGE,(self.BORDER_LEFT_X,self.BORDER_LEFT_Y)), (self.BORDER_IMAGE,(self.BORDER_RIGHT_X,self.BORDER_RIGHT_Y))])
        self.font_surface = self.FONT.render("Score: " + str(self.points),False,RED)
        self.score_board_image = pygame.draw.rect(self.WINDOW,BACKGROUND_COLOR,self.SCORE_BOARD)
        self.WINDOW.blit(self.font_surface,(self.BORDER_RIGHT_X+self.BORDER_THICKNESS,0))

class Slime(Map):
    def __init__(self):
        super().__init__()
        self.SLIME_SIZE = 100
        self.x = (self.WINDOW_WIDTH/2) - (self.SLIME_SIZE/2)
        self.y = self.WINDOW_HEIGHT-self.SLIME_SIZE
        self.left_move = True
        self.SLIME_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join("character_right_image.png")).convert_alpha(),(self.SLIME_SIZE,self.SLIME_SIZE))
        self.SLIME_LEFT = pygame.transform.scale(pygame.image.load(os.path.join("character_left_image.png")).convert_alpha(),(self.SLIME_SIZE,self.SLIME_SIZE))

    def draw(self):
        if self.left_move == False:
            self.WINDOW.blit(self.SLIME_RIGHT,(self.x,self.y))
        else:
            self.WINDOW.blit(self.SLIME_LEFT,(self.x,self.y))

class Star(Map):
    def __init__(self):
        super().__init__()
        self.STAR_SIZE = 60
        self.x = random.randint(self.BORDER_LEFT_X + self.BORDER_THICKNESS,self.BORDER_RIGHT_X - self.STAR_SIZE)
        self.y = -(self.STAR_SIZE)
        self.STAR = pygame.transform.scale(pygame.image.load(os.path.join("star_image.png")).convert_alpha(),(self.STAR_SIZE,self.STAR_SIZE))

    def movement(self,star_movement_speed):
        self.y += star_movement_speed

    def create_star(self):
        return Star()

    def draw(self):
        self.WINDOW.blit(self.STAR,(self.x,self.y))

def main():
    now = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps = 60
    score = 0
    run = True
    slime_movement_speed = 5
    star_movement_speed = 2

    map = Map()
    slime = Slime()
    star = Star()
    star_list_object = []
        
    while run:
        frame.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Give player control over the character on screen using keyboard's inputs.
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_LEFT]:
            slime.x -= slime_movement_speed
            slime.left_move = True
        if key_pressed[pygame.K_RIGHT]:
            slime.x += slime_movement_speed
            slime.left_move = False
        if key_pressed[pygame.K_SPACE]:
            run = False

        # This doesn't allow the player to go over the borders and the map
        if slime.x < map.BORDER_LEFT_X + map.BORDER_THICKNESS + slime_movement_speed:
            slime.x = map.BORDER_LEFT_X + map.BORDER_THICKNESS
        if slime.x > map.BORDER_RIGHT_X - slime.SLIME_SIZE - slime_movement_speed:
            slime.x = map.BORDER_RIGHT_X - slime.SLIME_SIZE
        if slime.y > map.WINDOW_HEIGHT - slime.SLIME_SIZE:
            slime.y = map.WINDOW_HEIGHT-slime.SLIME_SIZE
        if slime.y < 0:
            slime.y = 0


        # Allow the slime to eat stars, if the slime ate the star, delete that star from the screen
        if len(star_list_object) > 0:
            for i, star_object in enumerate(star_list_object):
                if (slime.x <= star_object.x + (star.STAR_SIZE/2) <= slime.x + slime.SLIME_SIZE) and (slime.y <= (star_object.y + star.STAR_SIZE/2) <= slime.y + slime.SLIME_SIZE):
                    score = score + 1
                    map.score(score)
                    delete_star = star_list_object.pop(i)
                    del delete_star # Delete Star object
        
        # Delete Star's objects that passed the border
        if len(star_list_object) >= 5:
            for i, star_object in enumerate(star_list_object):
                if star_object.y > map.WINDOW_HEIGHT:   # If the star didn't get eaten by the slime and it's passed through the map, delete the star object
                    delete_star = star_list_object.pop(i)
                    del delete_star

        # Create star objects
        cooldown = pygame.time.get_ticks() - now
        if cooldown >= 4000:
            star_object = star.create_star()    #Call the create_star() method from the Star class
            star_list_object.append(star_object)
            now = pygame.time.get_ticks()

        # Make the stars falling down
        for i in range(len(star_list_object)):
            star_list_object[i].movement(star_movement_speed)

        # Display the game
        map.draw()
        slime.draw()
        for i in range(len(star_list_object)):
            star_list_object[i].draw()
        pygame.display.update()

if __name__ == "__main__":
    main()