import Button
import Constants
import json
import Globe
import pygame
import Level


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
        self.load_levels()

        self.score = 0

        self.completed = [False for x in range(len(self.levels))]
        with open("data.json", "r") as file:
            loaded = json.load(file)
            if not loaded["highest"] == -1:
                for x in range(loaded["highest"] + 1):
                    self.completed[x] = True

            self.score = loaded["score"]

        self.levelselect_buttons = self.generate_buttons()

        # What state is the menu in
        self.menu_state = 'main'

        self.GAME = None

        # Used to count when game is over or level is completed
        self.reset_counter = 0

    def load_levels(self):
        with open("level.json", "r") as file:
            self.levels = json.load(file)

    def generate_buttons(self):
        # Creates buttons for each of the levels
        pos = [96, 300]

        buttons = []

        for idx, level in enumerate(self.levels):
            buttons.append(Button.Button(Constants.cscale(pos[0] + 10, pos[1] + 10), Constants.cscale(80, 50), None,
                                         True, fill_color=(0, (level["id"] - 1) / len(self.levels) * 255, 255),
                                         text=str(level["id"]), border_thickness=int(Constants.posscale(6)),
                                         font=Constants.BIGBOI_FONT,
                                         text_color=(0, 255 - ((level["id"] - 1) / len(self.levels) * 255), 50),
                                         border_color=(255, 0, 0) if not self.completed[idx] else (0, 255, 0)))

            pos[0] += 100
            if pos[0] >= 950:
                pos[0] = 96
                pos[1] += 70

        return buttons

    def save_game(self):
        with open("data.json", "w") as file:
            completed = len([x for x in self.completed if x]) - 1
            json.dump({"highest": completed, "score": self.score}, file)

    def run_menu(self, screen):
        if self.menu_state == 'main' or self.menu_state == 'level select':
            self.run_main(screen)
        elif self.menu_state == 'game':
            self.GAME.run_level(screen)

            if self.GAME.reset:
                self.reset_counter += 1

                if self.reset_counter > 50:
                    self.reset_counter = 0
                    self.start_game(self.GAME.json["id"] - 1)

            elif self.GAME.complete:
                self.score += (self.GAME.time_diff * 100) if not self.completed[self.GAME.json["id"] - 1] else 0
                self.completed[self.GAME.json["id"] - 1] = True
                self.levelselect_buttons[self.GAME.json["id"] - 1].set_colors(border_color=(0, 255, 0))
                if self.GAME.json["id"] + 1 > len(self.levels):
                    Constants.BIRTHDAY = True
                    self.menu_state = "main"
                else:
                    self.start_game(self.GAME.json["id"])
                self.save_game()

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
                        for idx in range(len(self.completed)):
                            if not self.completed[idx]:
                                self.start_game(idx)
                                return
                    if self.lvlsel_bttn.is_clicked(event.pos):
                        self.menu_state = 'level select'

        # Draw play Button and level select button
        if self.menu_state == 'main':
            self.play_button.draw(screen)
            self.lvlsel_bttn.draw(screen)
            self.play_button.is_hover(pygame.mouse.get_pos())
            self.lvlsel_bttn.is_hover(pygame.mouse.get_pos())

            # Draws score
            rendered_text = Constants.get_impact(Constants.cscale(35)).render("Score: " + str(self.score), False, (0, 0, 0))
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
            if not idx == 0:
                if not self.completed[idx - 1]:
                    screen.blit(Constants.LOCK_IMAGE, Constants.LOCK_IMAGE.get_rect(center=button.button_rect.center))

        for event in Globe.events:
            for idx, button in enumerate(self.levelselect_buttons):
                # Checks for presses on buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.is_clicked(event.pos):
                        if idx == 0 or self.completed[idx - 1]:
                            self.start_game(idx)
                            return

            if event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.is_clicked(event.pos):
                    self.menu_state = 'main'

    def start_game(self, idx):
        self.load_levels()
        self.GAME = Level.Level(self.levels[idx])
        self.menu_state = 'game'
