import pygame
import Globe
import Constants
import Sprite
import random

screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
Constants.convert()
Globe.start_app()

clock = pygame.time.Clock()
fps = 0
last_fps_show = 0

# Birthday screen stuff
balloons = [[random.randint(20, 1010), random.randint(20, 680), random.randint(3, 12)] for x in range(5)]
balloon_time = 0
inflation = Sprite.InflateSurface(None, 0, {}, Constants.BDAY_TEXT, .01, 1, 35, Constants.cscale(515, 90))

while Globe.running:
    screen.fill((111, 80, 51))

    Globe.events = pygame.event.get()

    if not Constants.BIRTHDAY:
        Globe.MENU.run_menu(screen)
    else:
        screen.blit(Constants.BDAY_BACKGROUND, (0, 0))
        inflation.run_sprite(screen, False)
        for ball in balloons:
            screen.blit(Constants.BDAY_BALLOON, Constants.BDAY_BALLOON.get_rect(center=Constants.cscale(ball[0], ball[1])))
            ball[1] -= ball[2]
        balloon_time += 1
        if balloon_time % 10 == 0:
            balloons.append([random.randint(20, 1010), 1000, random.randint(3, 12)])

    for event in Globe.events:
        if event.type == pygame.QUIT:
            Globe.running = False
            Globe.MENU.save_game()

    pygame.display.update()

    # sets fps to a variable. can be set to caption any time for testing.
    last_fps_show += 1
    if last_fps_show == 30:  # every 30th frame:
        fps = clock.get_fps()
        pygame.display.set_caption("Silverball v.2.0" + "   FPS: " + str(fps))
        last_fps_show = 0

    # fps max 60
    clock.tick(45)
