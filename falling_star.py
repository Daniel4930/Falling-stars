import pygame, sys
from player import Player
from game import Game
from button import Button
from jump_platform import Platform
pygame.init()
pygame.display.init()

def main():
    time_1 = pygame.time.get_ticks()
    time_2 = pygame.time.get_ticks()
    frame = pygame.time.Clock()
    fps = 60
    run = True

    game = Game()
    slime = Player()
    start_button = Button("START", 100, 50, (game.WINDOW_WIDTH / 2) - (130 / 2), (game.WINDOW_HEIGHT / 2) - 50)
    resume_button = Button("RESUME", 120, 50, (game.WINDOW_WIDTH / 2) - 120 / 2, (game.WINDOW_HEIGHT / 2) - 100)
    new_game_button = Button("NEW GAME", 150, 50, (game.WINDOW_WIDTH / 2) - 150 / 2, (game.WINDOW_HEIGHT / 2))
    exit_button = Button("EXIT GAME", 150, 50, (game.WINDOW_WIDTH / 2) - 150 / 2, (game.WINDOW_HEIGHT / 2) + 100)
    button_list = []
    button_list.append(start_button)
    button_list.append(resume_button)
    button_list.append(exit_button)
    button_list.append(new_game_button)
    button_group = pygame.sprite.Group()
    slime_single_group = pygame.sprite.GroupSingle()
    slime_single_group.add(slime)
    star_group = pygame.sprite.Group()

    platform1 = Platform(game.BORDER_LEFT_X + game.BORDER_THICKNESS + 10, game.WINDOW_HEIGHT / 2 + 130)
    platform2 = Platform(game.WINDOW_WIDTH / 2, game.WINDOW_HEIGHT - platform1.height - 30)
    platform3 = Platform(game.WINDOW_WIDTH / 2 - platform1.width / 2 + 150, game.WINDOW_HEIGHT / 2)
    platform4 = Platform(game.BORDER_LEFT_X + game.BORDER_THICKNESS, game.WINDOW_HEIGHT / 2)
    platform5 = Platform(game.BORDER_LEFT_X + game.BORDER_THICKNESS, game.WINDOW_HEIGHT / 2 - 182)
    platform_list = []
    platform_list.append(platform1)
    platform_list.append(platform2)
    platform_list.append(platform3)
    platform_list.append(platform4)
    platform_list.append(platform5)
    platform_group = pygame.sprite.Group()
        
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if game.game_state == "On home screen":
                    game.mouse_clicked(button_group)
                    if game.game_state == "Exit home screen":
                        star_group.empty()
                        button_group.empty()
                        game.exist_start_screen()
                        game.game_state = "Playing"
                        game.current_level(platform_group, platform_list)

                if game.game_state == "Pause":
                    game.mouse_clicked(button_group)
                    if game.game_state == "On home screen":
                        game.reset_game(star_group, platform_group, button_group)
                        slime_single_group.empty()
                        slime = Player()
                        slime_single_group.add(slime)
                        
        if game.game_state == "On home screen":
            cooldown_spawn_star = pygame.time.get_ticks() - time_1
            if cooldown_spawn_star >= 7000:
                game.spawn_blue_star(star_group)
                time_1 = pygame.time.get_ticks()
            button_group.add(start_button)
            button_group.add(exit_button)
            game.draw_starting_screen(star_group, button_group)
            pygame.display.update()
            frame.tick(fps)

        elif game.game_state == "Pause":
            if len(button_group.sprites()) == 0:
                button_group.add([button_list[1], button_list[2]], button_list[3])
            game.draw_pause_screen(button_group)
            pygame.display.update()
            frame.tick(fps)

        elif game.game_state == "Playing":
            cooldown_spawn_star = pygame.time.get_ticks() - time_1
            if cooldown_spawn_star >= 3000:
                game.spawn_blue_star(star_group)
                time_1 = pygame.time.get_ticks()

            cooldown_spawn_spinning_star = pygame.time.get_ticks() - time_2
            if cooldown_spawn_spinning_star >= game.spin_star_spawn_rate:
                game.spawn_yellow_star(star_group, slime)
                time_2 = pygame.time.get_ticks()

            game.star_and_platform_collision(platform_group, star_group)
            slime.slime_on_ground()
            slime.free_fall()
            slime.collision_platform(slime, platform_group)
            game.remove_star_outside_map(star_group)
            slime.input()
            game.check_game_state()
            game.slime_and_stars_collision(slime, star_group, platform_group, platform_list)
            game.draw(slime, star_group, slime_single_group, platform_group)
            pygame.display.update()
            frame.tick(fps)

        elif game.game_state == "Exit":
            print("Game Over\nScore: " + str(game.score))
            run = False
            sys.exit()

if __name__ == "__main__":
    main()