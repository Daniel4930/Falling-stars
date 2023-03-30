import pygame, sys
from slime import Slime
from game import Game
from button import Button
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
    button = Button("START")
    button_single_group = pygame.sprite.GroupSingle()
    button_single_group.add(button)
    slime_single_group = pygame.sprite.GroupSingle()
    slime_single_group.add(slime)
    star_group = pygame.sprite.Group()
        
    while run:
        for event in pygame.event.get():
            # To stop the game, click the close button on the window
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if game.game_state == "On home screen":
                    exit_menu = game.mouse_clicked(button.x, button.y, button.width, button.height)
                    if exit_menu == True:
                        game.exist_menu_screen(star_group)

        if exit_menu == False:
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 2000:
                game.spawn_star(star_group)
                now = pygame.time.get_ticks()
            game.draw_starting_page(star_group, button_single_group, button.text, button.x, button.y)
            pygame.display.update()
            frame.tick(fps)

        else:
            # Create star sprites and store all sprites a group
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 3000:
                game.spawn_star(star_group)
                now = pygame.time.get_ticks()

            # If collided, increase the score by 1
            game.slime_and_stars_collision(slime, star_group)

            #If a star go outside the map, remove that star from sprite group
            game.remove_star(star_group)

            #Display the game
            game.draw(slime, star_group, slime_single_group)
            pygame.display.update()
            frame.tick(fps)

if __name__ == "__main__":
    main()