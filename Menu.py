import Button
import Constants
import json
import Globe
import pygame


# class that controls the entire main menu
class Menu:
    def __init__(self):
        # Background moving sky images
        self.skys = []
        self.skys.append(Constants.posscale(515, divisors=(1030,)))
        self.skys.append(Constants.posscale(1542, divisors=(1030,)))
        # Remove skys that are off screen
        self.sky_remove = []

        # Instantiate Playbutton and other buttons
        self.play_button = Button.Button(Constants.cscale(100, 230), Constants.cscale(180, 60),
                                         Constants.PLAY_BUTTON_IMAGE, state_quantity=2)
        self.lvlsel_bttn = Button.Button(Constants.cscale(300, 230), Constants.cscale(160, 55),
                                         Constants.LEVELS_BUTTON_IMAGE, state_quantity=2)

        # TRANSFER TO LEVEL CLASS
        #self.play_button_inlevel = Button([420, 400], inlevel_play_button_image, [300, 100], [180, 60])
        #self.next_level_button = Button([200, 400], next_level_button_image, [300, 100], [180, 60])
        #self.exit_button = Button([0, 0], exit_icon, [260, 260], [50, 50])

        self.back_button = Button.Button(Constants.cscale(515, 210), Constants.cscale(100, 30), None, box=True,
                                         text="BACK", border_thickness=Constants.cscale(4),
                                         font=Constants.get_impact(Constants.cscale(26)))
        self.right_button = Button.Button(Constants.cscale(900, 210), Constants.cscale(50, 30), None, box=True,
                                          text=">", border_thickness=Constants.cscale(4),
                                          font=Constants.get_impact(Constants.cscale(26)))
        self.left_button = Button.Button(Constants.cscale(100, 210), Constants.cscale(50, 30), None, box=True,
                                         text="<", border_thickness=Constants.cscale(4),
                                         font=Constants.get_impact(Constants.cscale(26)))
        self.levels = []
        with open("level.json", "r") as file:
            self.levels = json.load(file)

        self.completed = [False for x in range(len(self.levels))]

        self.levelselect_buttons = self.generate_buttons()

        # What state is the menu in
        self.menu_state = 'main'

    def generate_buttons(self):
        # Creates buttons for each of the levels
        pos = [96, 300]

        buttons = []

        for level in self.levels:
            buttons.append(Button.Button(Constants.cscale(pos[0] + 10, pos[1] + 10), Constants.cscale(80, 50), None,
                                         True, fill_color=(0, (level["id"] - 1) / len(self.levels) * 255, 255),
                                         text=str(level["id"]), border_thickness=int(Constants.posscale(6)),
                                         font=Constants.BIGBOI_FONT,
                                         text_color=(0, 255 - ((level["id"] - 1) / len(self.levels) * 255), 50),
                                         border_color=(255, 0, 0)))

            pos[0] += 100
            if pos[0] >= 950:
                pos[0] = 96
                pos[1] += 70

        return buttons

    def run_menu(self, screen):
        if self.menu_state == 'main' or self.menu_state == 'level select':
            self.run_main(screen)
        elif self.menu_state == 'inlevel' or self.menu_state == 'postlevel':
            self.draw_inlevel(screen)

    def run_main(self, screen):
        self.sky_remove = []

        # Find off-screen skies and draw skies
        for idx, sky in enumerate(self.skys):
            screen.blit(Constants.MENU_SKY_IMAGE, (int(sky - Constants.posscale(515, divisors=(1030,))), 0))
            self.skys[idx] -= 1
            if sky <= Constants.posscale(-515, divisors=(1030,)):
                # 1 is subtracted to compensate for subtracting the 1 above
                self.sky_remove.append(sky - 1)

        # remove skys that need removing and adds a new sky to continue the loop
        for sky in self.sky_remove:
            if sky in self.skys:
                self.skys.remove(sky)
                self.skys.append(Constants.posscale(1533, divisors=(1030,)))

        # Draw foreground
        screen.blit(Constants.MENU_FOREGROUND_IMAGE, Constants.cscale(0, 0))

        # Menu Button events
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.menu_state == "main":
                    if self.play_button.is_clicked(event.pos):
                        # Takes you to the next uncompleted level
                        pass
                    if self.lvlsel_bttn.is_clicked(event.pos):
                        self.menu_state = 'level select'

        # Draw play Button and level select button
        if self.menu_state == 'main':
            self.play_button.draw(screen)
            self.lvlsel_bttn.draw(screen)
            self.play_button.is_hover(pygame.mouse.get_pos())
            self.lvlsel_bttn.is_hover(pygame.mouse.get_pos())

            # Draws score
            rendered_text = Constants.get_impact(Constants.cscale(35)).render("Score: " + str("NO WORK YET"), False, (0, 0, 0))
            screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(750, 250)))

        # redirects to another function to draw level selection related things
        elif self.menu_state == 'level select':
            self.draw_level_select(screen)

    def draw_level_select(self, screen):
        # draws button to go back to the main menu
        self.back_button.draw(screen)
        self.back_button.is_hover(pygame.mouse.get_pos())

        for idx, button in enumerate(self.levelselect_buttons):
            # Draws buttons
            button.draw(screen)
            button.is_hover(pygame.mouse.get_pos())

        # draws all the level buttons
        for event in Globe.events:
            for idx, button in enumerate(self.levelselect_buttons):
                # Checks for presses on buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.is_clicked(event.pos):
                        print(self.levels[idx]["id"])

            if event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.is_clicked(event.pos):
                    self.menu_state = 'main'

    def draw_inlevel(self, c):
        pass

        # Remake in level class
        '''if self.menustate == 'inlevel':
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
        '''
