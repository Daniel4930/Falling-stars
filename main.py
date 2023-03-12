import pygame, sys
from slime import Slime
from game import Game
from star import Star
pygame.init()
pygame.display.init()

def main():
    now = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps, score = 60, 0
    run, menu = True, True
    exit_menu = False

    game = Game()
    slime = Slime()
    slime_group = pygame.sprite.Group()
    slime_group.add(slime)
    star = Star()
    star_group = pygame.sprite.Group()
    star_group.add(star)
        
    while run:
        for event in pygame.event.get():
            # To stop the game, click the red button on the window
            if event.type == pygame.QUIT:
                run = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                menu = game.menu_screen(menu)
                if menu == False:
                    exit_menu = True

        #If existing menu screen, remove all stars from sprite group, then clear screen
        if menu == False and exit_menu == True:
            game.exist_menu_screen(star_group)
            exit_menu = False #Set exit_menu to False because it prevent this if statement from repeating

        #Starting menu screen of the game
        if menu:
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 2000:
                star.create_star(star_group)
                now = pygame.time.get_ticks()
            game.WINDOW.fill((0,0,0))
            game.draw_menu()
            star_group.draw(game.WINDOW)
            star_group.update()
            star.remove_star(star_group)
            pygame.display.update()
            frame.tick(fps)
        else:
            # Create star sprites and store all sprites a group
            cooldown = pygame.time.get_ticks() - now
            if cooldown >= 3000:
                star.create_star(star_group)
                now = pygame.time.get_ticks()

            # If collided, increase the score by 1
            collided_stars = slime.collision(slime, star_group)
            score += len(collided_stars)
            game.update_score(score)

            #If a star go outside the map, remove that star from sprite group
            star.remove_star(star_group)
            
            # Display the game
            game.WINDOW.fill((0,0,0))
            game.draw()
            slime.input()
            slime_group.draw(game.WINDOW)
            slime_group.update()
            star_group.draw(game.WINDOW)
            star_group.update()
            pygame.display.update()
            frame.tick(fps)

if __name__ == "__main__":
    main()