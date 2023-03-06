import pygame, random, sys
from slime import Slime
from game import Game
from star import Star
pygame.init()
pygame.display.init()

def main():
    now = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps = 60
    score = 0
    run = True

    game = Game()
    slime = Slime()
    slime_group = pygame.sprite.Group()
    slime_group.add(slime)
    star_group = pygame.sprite.Group()
        
    while run:
        for event in pygame.event.get():
            # To stop the game, click the red button on the window
            if event.type == pygame.QUIT:
                run = True
                sys.exit()
                
        # Create star sprites and store all sprites a group
        cooldown = pygame.time.get_ticks() - now
        if cooldown >= 4000:
            star_group.add(Star())
            now = pygame.time.get_ticks()

        # If collided, increase the score by 1
        collided_stars = slime.collision(slime, star_group)
        for num_star in collided_stars:
            score += 1
        
        # Display the game
        game.draw(score)
        slime.input()
        slime_group.draw(game.WINDOW)
        slime_group.update()
        star_group.draw(game.WINDOW)
        star_group.update()
        pygame.display.update()
        frame.tick(fps)

if __name__ == "__main__":
    main()