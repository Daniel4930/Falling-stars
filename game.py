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
        self.enable_screen_transition = True
        self.game_state = "On home screen"
        self.spin_star_spawn_rate = 4000

        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        self.BORDER_IMAGE = pygame.image.load(os.path.join("images", "wall_border.png")).convert_alpha()
        self.BACKGROUND_IMAGE = pygame.image.load(os.path.join("images", "background.png")).convert_alpha()
        self.MENU_IMAGE = pygame.image.load(os.path.join("images", "menu_image.png"))
        self.GAME_TITILE = pygame.display.set_caption("Falling Stars")
        self.FONT = pygame.font.SysFont('Arial',22)
        self.SCREEN_TRANSITION = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

    # Check if mouse clicked on the button
    def mouse_clicked(self, button_group):
        list = button_group.sprites()
        for i in range(len(list)):
            if list[i].rect.collidepoint(pygame.mouse.get_pos()):
                if list[i].text == "START":
                    self.game_state = "Exit home screen"
                elif list[i].text == "RESUME":
                    self.game_state = "Playing"
                    pygame.mouse.set_visible(False)
                elif list[i].text == "NEW GAME":
                    self.game_state = "On home screen"
                elif list[i].text == "EXIT GAME":
                    self.game_state = "Exit"
    
    def draw_starting_screen(self, star_group, button_group):   
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blit(self.MENU_IMAGE, (0,0))
        button_group.draw(self.WINDOW)
        star_group.draw(self.WINDOW)
        button_group.update()
        star_group.update(self.level)
            
    def exist_start_screen(self):
        pygame.mouse.set_visible(False)
        copy_of_current_screen = pygame.Surface.copy(self.WINDOW)
        if self.enable_screen_transition:
            self.screen_transition(copy_of_current_screen)
        self.enable_screen_transition = True
        self.game_state = "Playing"

    def clear_level(self, star_group, slime):
        star_group.empty()
        slime.return_to_spawn_point()
        copy_of_current_screen = pygame.Surface.copy(self.WINDOW)
        self.screen_transition(copy_of_current_screen)

    def screen_transition(self, copy_of_current_window_screen):
        self.SCREEN_TRANSITION.fill(self.BLACK)
        while self.alpha <= 255:
            self.alpha += 2
            self.WINDOW.blit(copy_of_current_window_screen, (0,0))
            self.SCREEN_TRANSITION.set_alpha(self.alpha)
            self.WINDOW.blit(self.SCREEN_TRANSITION, (0,0))
            pygame.display.update()
        self.alpha = 0

    def check_game_state(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self.game_state = "Pause"

    def draw_pause_screen(self, button_group):
        pygame.mouse.set_visible(True)
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blit(self.BACKGROUND_IMAGE, (0,0))
        button_group.draw(self.WINDOW)
        button_group.update()

    def current_level(self, platform_group, platform_list):
        if self.level == 1 and self.increase_difficulty:
            platform_group.add([platform_list[0], platform_list[1], platform_list[2]])

        elif self.level == 2 and self.increase_difficulty:
            platform_list[3].y = platform_list[2].y + 50
            platform_list[2].y = self.WINDOW_HEIGHT / 2 - 100
            platform_list[3].platform_moving()
            platform_group.add(platform_list[3])
            platform_list[0].y = 550

        elif self.level == 3 and self.increase_difficulty:
            platform_list[4].rotate_platform()
            platform_list[2].x = self.WINDOW_WIDTH / 2 - 100
            platform_group.add(platform_list[4])

        self.increase_difficulty = False

        if self.level == 1:
            self.spin_star_spawn_rate = 4000
        elif self.level == 2:
            self.spin_star_spawn_rate = 2000
        elif self.level == 3:
            self.spin_star_spawn_rate = 1000

    def level_up(self, slime, star_group, platform_group, platform_list):
        if self.score == 5 or self.score == 10:
            self.level += 1
            self.increase_difficulty = True
            self.enable_screen_transition = False
            self.clear_level(star_group, slime)
            self.current_level(platform_group, platform_list)
            
    def spawn_blue_star(self, star_group):
        star_group.add(Star(random.randrange(self.BORDER_LEFT_X + self.BORDER_THICKNESS, self.BORDER_RIGHT_X - self.STAR_SIZE), -(self.STAR_SIZE), 1, False))

    def spawn_yellow_star(self, star_group, slime):
        window_side = random.randrange(1,4)

        if window_side == 1: #Spawn from the top
            star_group.add(Star(random.randrange(slime.x, slime.x + self.SLIME_WIDTH), -(self.STAR_SIZE), window_side, True))
            
        elif window_side == 2: #Spawn from the right
            if self.WINDOW_HEIGHT - self.STAR_SIZE <= (slime.y + self.SLIME_HEIGHT) <= self.WINDOW_HEIGHT:
                star_group.add(Star(self.WINDOW_WIDTH + self.STAR_SIZE, self.WINDOW_HEIGHT - self.STAR_SIZE, window_side, True))
            else:
                star_group.add(Star(self.WINDOW_WIDTH + self.STAR_SIZE, random.randrange(slime.y, slime.y + self.SLIME_HEIGHT), window_side, True))
        
        elif window_side == 3: #Spawn from the left
            if self.WINDOW_HEIGHT - self.STAR_SIZE <= (slime.y + self.SLIME_HEIGHT) <= self.WINDOW_HEIGHT:
                star_group.add(Star(-self.STAR_SIZE, self.WINDOW_HEIGHT - self.STAR_SIZE, window_side, True))
            else:
                star_group.add(Star( -self.STAR_SIZE, random.randrange(slime.y, slime.y + self.SLIME_HEIGHT), window_side, True))
    
    def remove_star_outside_map(self, star_group):
        list = star_group.sprites()
        for i in range(len(list)):
            if list[i].is_animated == False:
                if list[i].y > self.WINDOW_HEIGHT:
                    star_group.remove(list[i])
            else:
                if list[i].initial_position == 1:
                    if list[i].y > self.WINDOW_HEIGHT:
                        star_group.remove(list[i])
                elif list[i].initial_position == 2:
                    if list[i].x < -(self.STAR_SIZE):
                        star_group.remove(list[i])
                elif list[i].initial_position == 3:
                    if list[i].y < -(self.STAR_SIZE):
                        star_group.remove(list[i])
                else:
                    if list[i].x > self.WINDOW_WIDTH + self.STAR_SIZE:
                        star_group.remove(list[i])

    def star_and_platform_collision(self, platform_group, star_group):
        all_star = star_group.sprites()
        all_platform = platform_group.sprites()
        for i in range(len(all_star)):
            for y in range(len(all_platform)):
                if pygame.sprite.collide_rect(all_star[i], all_platform[y]):
                    if all_star[i].is_animated:
                        star_group.remove(all_star[i])
                    else: 
                        all_star[i].platform_collision(all_platform[y].y - self.STAR_SIZE)
                else:
                    all_star[i].no_platform_collision()

    def slime_and_stars_collision(self, slime, star_group, platform_group, platform_list):
        star_collided = slime.slime_star_collision(slime, star_group)
        for i in range(len(star_collided)):
            if star_collided[i].is_animated:
                slime.health -= 1
                slime.is_animated = True
                if slime.health == 0:
                    self.game_state = "Exit"
            else:
                self.score += len(star_collided)
                self.level_up(slime, star_group, platform_group, platform_list)
    
    def reset_game(self, star_group, platform_group, button_group):
        star_group.empty()
        platform_group.empty()
        button_group.empty()
        self.score = 0
        self.level = 1
        self.increase_difficulty = True

    def draw(self, slime, star_group, slime_single_group, platform_group):
        score_text_surface = self.FONT.render("Score: " + str(self.score), True, self.RED)
        level_text_surface = self.FONT.render("Level: " + str(self.level), True, self.RED)
        heath_text_surface = self.FONT.render("Health: " + str(slime.health), True, self.RED)
        self.WINDOW.fill(self.BLACK)
        self.WINDOW.blits([(self.BACKGROUND_IMAGE, (0,0)), 
                           (self.BORDER_IMAGE, (self.BORDER_LEFT_X, self.BORDER_LEFT_Y)), 
                           (self.BORDER_IMAGE, (self.BORDER_RIGHT_X, self.BORDER_RIGHT_Y)),
                           (score_text_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 0)),
                           (level_text_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 30)),
                           (heath_text_surface, (self.BORDER_RIGHT_X + self.BORDER_THICKNESS, 60))])
        slime_single_group.draw(self.WINDOW)
        platform_group.draw(self.WINDOW)
        star_group.draw(self.WINDOW)
        slime_single_group.update()
        platform_group.update()
        star_group.update(self.level)