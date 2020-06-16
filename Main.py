import math
import pygame
import time
import os
# Other python files

import Button
import Global

pygame.init()
print(pygame.ver)

# BASIC PYGAME STUFF
# Screen size
screen = pygame.display.set_mode((1030, 700), pygame.DOUBLEBUF)
# Window Caption
pygame.display.set_caption("SilverBall")
# Constant game clock mainly for FPS measuring
clock = pygame.time.Clock()
# If set to true, game will exit
crashed = False

#fonts
def ComicSans(size):
    return pygame.font.SysFont('Comic Sans MS', size)

# class that controls the entire main menu
class Menu:
    def __init__(self):
        # Background moving sky images
        self.skys = []
        self.skys.append(515)
        self.skys.append(1542)
        # Remove skys that are off screen
        self.sky_remove = []

        # Instantiate Playbutton and other buttons ------TEMPORARILY COMMENTED OUT
        self.play_button = Button.Button([150, 230], GLOBAL.play_button_image, [150, 50])
        self.lvlsel_bttn = Button.Button([450, 240], GLOBAL.levelsel_button_image, [160, 55])

        self.play_button_inlevel = Button.Button([420, 400], GLOBAL.inlevel_play_button_image, [180, 60])
        self.next_level_button = Button.Button([200, 400], GLOBAL.next_level_button_image, [180, 60])
        # self.exit_button = Button([0,0],exit_icon,[260,260],[50,50])

        self.levelselect_buttons = []
        self.back_button = Button.Button([515, 210], 'rect', [100, 30], (0,0,0), (192,192,192), 'BACK', 20, (0,0,0))
        self.right_button = Button.Button([900, 210], 'rect', [50, 30], (0,0,0), (192,192,192), '>', 20, (0,0,0))
        self.left_button = Button.Button([100, 210], 'rect', [50, 30], (0,0,0), (192,192,192), '<', 20, (0,0,0))

        # What state is the menu in
        self.menustate = 'main'

        # used to track what page you're on when on level select
        self.page = 1

    def draw(self):
        if self.menustate == 'main' or self.menustate == 'level select':
            self.draw_main()
        elif self.menustate == 'inlevel' or self.menustate == 'postlevel':
            self.draw_inlevel()

    def draw_main(self):
        self.sky_remove = []

        # Find off screen skys and draw skys
        for idx, sky in enumerate(self.skys):
            screen.blit(GLOBAL.menu_sky, [sky - 515, 0])
            self.skys[idx] -= 1
            if sky <= -515:
                # 1 is subtracted to compensate for subtracting the 1 above
                self.sky_remove.append(sky - 1)

        # remove skys that need removing and adds a new sky to continue the loop
        for sky in self.sky_remove:
            if sky in self.skys:
                self.skys.remove(sky)
                self.skys.append(1533)

        # Draw foreground
        screen.blit(GLOBAL.menu_image, [0, 0])

        # Draw play Button and level select button ------------TEMPORARILY COMMENTED OUT BUTTON DRAWS AND SCORE DRAW
        if self.menustate == 'main':
            self.play_button.draw(screen)
            self.lvlsel_bttn.draw(screen)

        # redirects to another function to draw level selection related things
        elif self.menustate == 'level select':
            self.draw_levelselect()
        '''
        #Draws score
        if self.menustate == 'main':
            c.draw_text("SCORE:" + str(GLOBAL.score),[650,250],45,'Black','monospace')'''

    def draw_levelselect(self):
        # draws all the level buttons
        for idx, button in enumerate(self.levelselect_buttons):
            if GLOBAL.completed[idx] == True:
                button.outline = 'Green'
            else:
                button.outline = 'Red'
            button.draw()

        # draws button to go back to the main menu
        self.back_button.draw(screen)

        # draws right and left arrow buttons if they are needed
        if len(self.levelselect_buttons) > 80 * self.page:
            self.right_button.draw(screen)
        if self.page > 1:
            self.left_button.draw(screen)

        screen.blit(ComicSans(30).render('Page ' + str(self.page),False,(0,0,0)),(620,190))

    '''def draw_inlevel(self, c):
        # When on the start level screen, this draws the level for preview
        ###################################
        ###################################
        ######FOR LEVEL PREVIEW############
        ###################################
        ###################################
        # Variable used to track current position on grid when drawing level
        self.grid_position = [40, 40]

        # Draw Marble
        c.draw_image(marble_image, [515, 350], [1030, 700], [515, 350], [1030, 700])

        # Draws water shadows
        for row in GLOBAL.CURRENT_LVL.ground_layout:
            for tile in row:
                if tile == 'T' or tile == 'B' or tile == 'S':
                    c.draw_image(water_shadow, [260, 260], [520, 520],
                                 [self.grid_position[0] + 25, self.grid_position[1] + 25], [100, 100])
                self.grid_position[0] += 50
            self.grid_position[1] += 50
            self.grid_position[0] = 40

            # Draw Boxes before tiles for sink effect
        for box in GLOBAL.CURRENT_LVL.boxes:
            if box.state == 'drown':
                box.draw(c)

        # Draw Water
        c.draw_image(water_image, [515, 350], [1030, 700], [515, 350], [1030, 700])

        # Reset Grid Position
        self.grid_position = [40, 40]

        # Draws the ground_layout
        for row in GLOBAL.CURRENT_LVL.ground_layout:
            for tile in row:
                c.draw_image(tile_dictionary[tile], [130, 130], [260, 260], self.grid_position, [50, 50])
                self.grid_position[0] += 50
            self.grid_position[1] += 50
            self.grid_position[0] = 40

            # Draws any X tiles
        for tile in GLOBAL.CURRENT_LVL.xice:
            tile.draw(c)
        for tile in GLOBAL.CURRENT_LVL.xbox:
            tile.draw(c)

        # Draws boxes
        for box in GLOBAL.CURRENT_LVL.boxes:
            if not box.state == 'drown':
                box.draw(c)

        # Draws HotBar Items and Border
        c.draw_image(border_image, [515, 350], [1030, 700], [515, 350], [1030, 700])
        c.draw_polygon([[100, 640], [300, 640], [300, 698], [100, 698]], 5, 'Black')
        c.draw_text('TIME: ' + str(GLOBAL.CURRENT_LVL.time), [115, 680], 40, 'Black')
        c.draw_polygon([[300, 640], [500, 640], [500, 698], [300, 698]], 5, 'Black')
        c.draw_text('LEVEL ' + str(GLOBAL.CURRENT_LVL_IDX + 1), [315, 680], 40, 'Black')
        self.exit_button.center = [550, 665]
        self.exit_button.draw(c)

        if self.menustate == 'inlevel':
            # Draws info box on start of level
            c.draw_polygon([[300, 150], [730, 150], [730, 500], [300, 500]], 3, 'Black', 'rgb(205,175,149)')
            c.draw_text('~*SILVERBALL*~', [315, 210], 50, 'Black')
            c.draw_text('LEVEL: ' + str(GLOBAL.CURRENT_LVL_IDX + 1), [465, 235], 25, 'Black')
            c.draw_text('NAME', [478, 318], 25, 'Black', 'sans-serif')
            c.draw_text('_____', [479, 317], 25, 'Black', 'sans-serif')
            c.draw_text(GLOBAL.CURRENT_LVL.name, [420, 350], 35, 'Black', 'sans-serif')
            self.play_button_inlevel.center = [515, 430]
            self.play_button_inlevel.draw(c)

        elif self.menustate == 'postlevel':
            c.draw_polygon([[50, 100], [300, 100], [300, 550], [50, 550]], 3, 'Black', 'rgb(205,175,149)')
            c.draw_text('LEVEL ' + str(GLOBAL.CURRENT_LVL_IDX + 1), [90, 155], 33, 'Black')
            c.draw_text('COMPLETE!!', [70, 187], 33, 'Black')
            c.draw_text('SCORE:', [53, 260], 30, 'Black', 'monospace')
            c.draw_text(str(GLOBAL.current_score), [53, 295], 30, 'Black', 'monospace')
            c.draw_text('TOTAL SCORE:', [53, 345], 30, 'Black', 'monospace')
            c.draw_text(str(GLOBAL.score), [53, 380], 30, 'Black', 'monospace')
            self.next_level_button.center = [150, 500]
            self.next_level_button.draw(c)

        ###################################
        ###################################
        ######FOR LEVEL PREVIEW############
        ###################################
        ###################################'''

    def mouse(self, pos):
        # when in the main menu state
        if self.menustate == 'main':
            # if play button is pressed, menu state changes to preview the level. Level 1 is selected. Level is reset
            if self.play_button.click(pos):
                self.menustate = 'inlevel'
                GLOBAL.CURRENT_LVL_IDX = 0
                Game_Reset()
            elif self.lvlsel_bttn.click(pos):
                self.menustate = 'level select'

        elif self.menustate == 'level select':
            # detects when any of the level buttons are clicked in level select
            for idx, bttn in enumerate(self.levelselect_buttons):
                if bttn.click(pos):
                    self.menustate = 'inlevel'
                    GLOBAL.CURRENT_LVL_IDX = idx
                    Game_Reset()

            # Button to return to main menu from level select
            if self.back_button.click(pos):
                self.menustate = 'main'

            # Right and left arrow buttons to switch pages
            elif self.right_button.click(pos) and len(self.levelselect_buttons) > 80 * self.page:
                self.page += 1
                for button in self.levelselect_buttons:
                    button.center[1] -= 700

            elif self.left_button.click(pos) and self.page > 1:
                self.page -= 1
                for button in self.levelselect_buttons:
                    button.center[1] += 700

        elif self.menustate == 'inlevel':
            # When in level preview, press play to begin level
            if self.play_button_inlevel.click(pos):
                GLOBAL.gamestate = 'Ingame'
            # X button at bottom hotbar to exit to main menu
            elif self.exit_button.click(pos):
                self.menustate = 'main'

        elif self.menustate == 'postlevel':
            # X button at bottom hotbar to exit to main menu
            if self.exit_button.click(pos):
                self.menustate = 'main'
            # When level is beaten, press next level to move to next level.
            elif self.next_level_button.click(pos):
                if len(GLOBAL.levels) < GLOBAL.CURRENT_LVL_IDX + 2:
                    self.menustate = 'main'
                else:
                    GLOBAL.CURRENT_LVL_IDX += 1
                    Game_Reset()
                    self.menustate = 'inlevel'

# Class Instances
GLOBAL = Global.global_store(Menu())

GLOBAL.define_levels()
# make the completed list as long as the amount of levels
for level in GLOBAL.levels:
    GLOBAL.completed.append(False)

# A temporary variable that is used once to track button position as buttons are drawn
bttn_pos = [95.5, 300]

# adds level select buttons
for idx, level in enumerate(GLOBAL.levels):
    GLOBAL.MENU.levelselect_buttons.append(
        Button.Button(bttn_pos[:], 'rect', [87, 40], 'Red', 'rgb(102,144,178)', 'Level ' + str(idx + 1), 20, 'White'))
    bttn_pos[0] += 93
    if bttn_pos[0] >= 935:
        bttn_pos[1] += 50
        bttn_pos[0] = 95.5
    if bttn_pos[1] % 700 == 0:
        bttn_pos[1] += 300

def Game_Reset():
    global GLOBAL
    GLOBAL.define_levels()
    GLOBAL.CURRENT_LVL = GLOBAL.levels[GLOBAL.CURRENT_LVL_IDX]

# fps variable used within main loop
last_fps_show = 0
# Main loop
while not crashed:
    # event handling
    for event in pygame.event.get():
        # if X is pressed, quit game
        if event.type == pygame.QUIT:
            crashed = True

        # Detects Mouse Clicks and calls functions accordingly
        if event.type == pygame.MOUSEBUTTONDOWN:
            if GLOBAL.gamestate == 'Menu':
                GLOBAL.MENU.mouse(pygame.mouse.get_pos())
            if GLOBAL.gamestate == 'Ingame':
                GLOBAL.CURRENT_LVL.mouse(pygame.mouse.get_pos())

    # calls draw according to gamestate
    if GLOBAL.gamestate == 'Ingame':
        GLOBAL.CURRENT_LVL.draw_level()
    elif GLOBAL.gamestate == 'Menu':
        GLOBAL.MENU.draw()

    last_fps_show += 1
    if last_fps_show == 30:  # every 30th frame:
        pygame.display.set_caption(str(clock.get_fps()))
        last_fps_show = 0

    print(GLOBAL.MENU.menustate)

    # fps max 75
    clock.tick(75)
    # update the display
    pygame.display.update()

# once loop is terminated, pygame stops running
pygame.quit()
