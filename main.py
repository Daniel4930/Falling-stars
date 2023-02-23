import pygame, os, random, sys
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
    left_move, run = True, True

    game = Game()
    slime = Slime((game.WINDOW_WIDTH/2) - (game.SLIME_SIZE/2), (game.WINDOW_HEIGHT - game.SLIME_SIZE), left_move)
    slime_group = pygame.sprite.Group()
    slime_group.add(slime)
    star_group = pygame.sprite.Group()
        
    while run:
        frame.tick(fps)
        for event in pygame.event.get():
            # To stop the game, click the red button on the window
            if event.type == pygame.QUIT:
                run = True
                sys.exit()
                
        # Create star sprites and store all sprites a group
        cooldown = pygame.time.get_ticks() - now
        if cooldown >= 2000:
            new_star = Star(random.randrange(game.BORDER_LEFT_X + game.BORDER_THICKNESS, game.BORDER_RIGHT_X - game.STAR_SIZE), -(game.STAR_SIZE))
            star_group.add(new_star)
            now = pygame.time.get_ticks()

        # If collided, increase the score by 1
        collided_stars = slime.collision(slime, star_group)
        for num_star in collided_stars:
            score += 1
        
        # Display the game
        game.draw(score)
        slime_group.draw(game.WINDOW)
        slime_group.update()
        star_group.draw(game.WINDOW)
        star_group.update()
        pygame.display.update()

if __name__ == "__main__":
    main()