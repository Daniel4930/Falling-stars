import pygame, sys
from slime import Slime
from game import Game
from button import Button
from jump_platform import Platform
pygame.init()
pygame.display.init()

def main():
    now = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps = 60
    run = True
    exit_menu = False

    game = Game()
    slime = Slime()
    start_button = Button("START", 100, 50, (game.WINDOW_WIDTH / 2) - (130 / 2), (game.WINDOW_HEIGHT / 2) - 50)
    button_single_group = pygame.sprite.GroupSingle()
    button_single_group.add(start_button)
    slime_single_group = pygame.sprite.GroupSingle()
    slime_single_group.add(slime)
    star_group = pygame.sprite.Group()

    platform1 = Platform(game.BORDER_LEFT_X + game.BORDER_THICKNESS, 450)
    platform2 = Platform(game.WINDOW_WIDTH / 2, game.WINDOW_HEIGHT - platform1.height)
    platform3 = Platform(game.WINDOW_WIDTH / 2 - platform1.width / 2, game.WINDOW_WIDTH / 2 - 250)
    platform4 = Platform(game.WINDOW_WIDTH / 2, 500)
    platform5 = Platform(game.WINDOW_WIDTH / 2, 620)
    platform_group = pygame.sprite.Group()
        
    while run:
        for event in pygame.event.get():
            # To stop the game, click the close button on the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if game.game_state == "On home screen":
                    exit_menu = game.mouse_clicked(start_button.x, start_button.y, start_button.width, start_button.height, start_button.text)
                    if exit_menu == True:
                        game.exist_menu_screen(star_group)

        if exit_menu == False: #Set this back to false after finish testing
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 2000:
                game.spawn_star(star_group)
                now = pygame.time.get_ticks()
            game.draw_starting_page(star_group, button_single_group, start_button.text, start_button.x, start_button.y)
            pygame.display.update()
            frame.tick(fps)

        else:

            game.current_level(platform_group, platform1, platform2, platform3, platform4, platform5)

            # Create star sprites and store all sprites a group
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 3000:
                game.spawn_star(star_group)
                now = pygame.time.get_ticks()

            #Check if a star collide with a platform
            #If so, let the star stay on top of the platform
            game.star_and_platform_collision(platform_group, star_group)

            #Check if the slime is on the ground
            #If not then the slime's state is mid air
            slime.slime_on_ground()

            # If collided with a star, increase the score by 1
            game.slime_and_stars_collision(slime, star_group)

            #Allow the slime to free-fall when in mid air
            slime.free_fall()

            # Allow player to jump onto platforms
            slime.collision_platform(slime, platform_group)

            #If a star go outside the map, remove that star from sprite group
            game.remove_star_outside_map(star_group)

            #Display the game
            game.draw(slime, star_group, slime_single_group, platform_group)
            pygame.display.update()
            frame.tick(fps)

if __name__ == "__main__":
    main()