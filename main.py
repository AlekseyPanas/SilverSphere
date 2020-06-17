import pygame
import Globe
import Constants

screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
Constants.convert()
Globe.start_app()

clock = pygame.time.Clock()
fps = 0
last_fps_show = 0

while Globe.running:
    screen.fill((0, 0, 255))

    Globe.events = pygame.event.get()

    Globe.MENU.run_menu(screen)

    for event in Globe.events:
        if event.type == pygame.QUIT:
            Globe.running = False

    pygame.display.update()

    # sets fps to a variable. can be set to caption any time for testing.
    last_fps_show += 1
    if last_fps_show == 30:  # every 30th frame:
        fps = clock.get_fps()
        pygame.display.set_caption("Silverball" + "   FPS: " + str(fps))
        last_fps_show = 0

    # fps max 60
    clock.tick(60)
