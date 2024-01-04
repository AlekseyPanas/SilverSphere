from __future__ import annotations
import Menu
import pygame
import math
import random
import Sprite
import Constants
import Button
from abc import abstractmethod
from dataclasses import dataclass


class DelayedAssetLoader:
    def __init__(self):
        self.__classes = []

    def register(self, obj_type: type):
        """Append attributes for delayed loading"""
        self.__classes.append(obj_type)

    def load(self):
        """Load the assets"""
        for obj in self.__classes
            for k in [k for k in obj.__dict__ if isinstance(obj.__dict__[k], PreAsset)]:  # Loop through PreAsset attributes
                asset = obj.__dict__[k]
                if asset.size is None:
                    setattr(obj, k, pygame.image.load(asset.path).convert_alpha())
                else:
                    setattr(obj, k, pygame.transform.smoothscale(pygame.image.load(asset.path),
                                                                 Constants.cscale(*asset.size)).convert_alpha())


@dataclass
class PreAsset:
    path: str
    size: tuple[int, int] = None


def register_assets(obj: type, asset_loader: DelayedAssetLoader):
    """Decorator for loading python image assets and converting them when defined as static
    variables in a class. The class is registered with a delayed loader which can then be called
    to inject the assets later"""




class Manager:

    def __init__(self, menu: Menu, **kwargs): pass

    @abstractmethod
    def run(self, screen: pygame.Surface, menu: Menu):
        """Given the screen and the parent Menu manager, perform one frame of execution"""

    def do_persist(self) -> bool:
        """Return if this instance should be reused on state change"""


class BirthdayManager(Manager):
    """Manager for Birthday Screen"""

    def __init__(self, menu: Menu):
        # Birthday screen stuff
        super().__init__(menu)
        self.balloons = [[random.randint(20, 1010), random.randint(20, 680), random.randint(3, 12)] for x in range(5)]
        self.balloon_time = 0
        self.inflation = Sprite.InflateSurface(None, 0, {}, Constants.BDAY_TEXT, .01, 1, 35, Constants.cscale(515, 90))

    def run(self, screen: pygame.Surface, menu: Menu):
        screen.blit(Constants.BDAY_BACKGROUND, (0, 0))
        self.inflation.run_sprite(screen, False)
        for ball in self.balloons:
            screen.blit(Constants.BDAY_BALLOON,
                        Constants.BDAY_BALLOON.get_rect(center=Constants.cscale(ball[0], ball[1])))
            ball[1] -= ball[2]
        self.balloon_time += 1
        if self.balloon_time % 10 == 0:
            self.balloons.append([random.randint(20, 1010), 1000, random.randint(3, 12)])

    def do_persist(self) -> bool: return False


class MenuScreenManager(Manager):
    """Manager for main menu screen"""
    def __init__(self, menu: Menu):
        super().__init__(menu)
        # Background moving sky images
        self.skys = []
        self.skys.append(Constants.posscale(515, divisors=(1030,)))
        self.skys.append(Constants.posscale(1542, divisors=(1030,)))
        # Remove skys that are off-screen
        self.sky_remove = []

    def run_menu_background(self, screen: pygame.Surface, menu: Menu):
        """Receives control first, blits menu BG animation"""
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

    @abstractmethod
    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        """Menu screen functionality core and event processing"""

    def run(self, screen: pygame.Surface, menu: Menu):
        self.run_menu_background(screen, menu)
        self.run_menu_foreground(screen, menu)

    def do_persist(self) -> bool: return True


@register_assets
class MenuScreenMainManager(MenuScreenManager):
    PLAY = PreAsset("./assets/menu_play_button.png")

    def __init__(self, menu: Menu):
        super().__init__(menu)
        # Instantiate Play button and other buttons
        self.play_button = Button.Button(Constants.cscale(100, 230), Constants.cscale(180, 60),
                                         Constants.PLAY_BUTTON_IMAGE, state_quantity=2)
        self.lvlsel_bttn = Button.Button(Constants.cscale(300, 230), Constants.cscale(160, 55),
                                         Constants.LEVELS_BUTTON_IMAGE, state_quantity=2)

    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        self.play_button.draw(screen)
        self.lvlsel_bttn.draw(screen)
        self.play_button.is_hover(pygame.mouse.get_pos())
        self.lvlsel_bttn.is_hover(pygame.mouse.get_pos())

        # Draws score
        rendered_text = Constants.get_impact(Constants.cscale(35)).render("Score: " + str(menu.score), False, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(750, 250)))

        screen.blit(screen, self.PLAY, (0, 0))

        # Menu Button events
        for event in menu.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_button.is_clicked(event.pos):
                    # Takes you to the next uncompleted level
                    for idx in range(len(menu.completed)):
                        if not menu.completed[idx]:
                            pass  # TODO: start game with idx

                elif self.lvlsel_bttn.is_clicked(event.pos):
                    pass  # TODO: Switch to level sel


class MenuScreenLevelSelectManager(MenuScreenManager):
    def __init__(self, menu: Menu):
        super().__init__(menu)
        self.back_button = Button.Button(Constants.cscale(515, 210), Constants.cscale(100, 30), None, box=True,
                                         text="BACK", border_thickness=Constants.cscale(4),
                                         font=Constants.get_impact(Constants.cscale(26)))
        self.right_button = Button.Button(Constants.cscale(900, 210), Constants.cscale(50, 30), None, box=True,
                                          text=">", border_thickness=Constants.cscale(4),
                                          font=Constants.get_impact(Constants.cscale(26)))
        self.left_button = Button.Button(Constants.cscale(100, 210), Constants.cscale(50, 30), None, box=True,
                                         text="<", border_thickness=Constants.cscale(4),
                                         font=Constants.get_impact(Constants.cscale(26)))

        # Load level buttons
        self.levelselect_buttons = self.generate_buttons(menu)

    def generate_buttons(self, menu: Menu):
        # Creates buttons for each of the levels
        pos = [96, 300]

        buttons = []

        for idx, level in enumerate(menu.levels):
            buttons.append(Button.Button(Constants.cscale(pos[0] + 10, pos[1] + 10), Constants.cscale(80, 50), None,
                                         True, fill_color=(0, (level["id"] - 1) / len(menu.levels) * 255, 255),
                                         text=str(level["id"]), border_thickness=int(Constants.posscale(6)),
                                         font=Constants.BIGBOI_FONT,
                                         text_color=(0, 255 - ((level["id"] - 1) / len(menu.levels) * 255), 50),
                                         border_color=(255, 0, 0) if not menu.completed[idx] else (0, 255, 0)))

            pos[0] += 100
            if pos[0] >= 950:
                pos[0] = 96
                pos[1] += 70

        return buttons

    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        # draws button to go back to the main menu
        self.back_button.draw(screen)
        self.back_button.is_hover(pygame.mouse.get_pos())

        for idx, button in enumerate(self.levelselect_buttons):
            # Draws buttons
            button.draw(screen)
            button.is_hover(pygame.mouse.get_pos())
            if not idx == 0:
                if not menu.completed[idx - 1]:
                    screen.blit(Constants.LOCK_IMAGE, Constants.LOCK_IMAGE.get_rect(center=button.button_rect.center))

        for event in menu.events:
            for idx, button in enumerate(self.levelselect_buttons):
                # Checks for presses on buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.is_clicked(event.pos):
                        if idx == 0 or menu.completed[idx - 1]:
                            pass  # TODO: start game with idx

            if event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.is_clicked(event.pos):
                    pass  # TODO: Switch to main


# TODO: Game-menu code

# self.game = None
#
# # Used to count when game is over or level is completed
# self.reset_counter = 0

# elif self.menu_state == 'game':
#     self.game.run_level(screen)
#
#     if self.game.reset:
#         self.reset_counter += 1
#
#         if self.reset_counter > 50:
#             self.reset_counter = 0
#             self.start_game(self.game.json["id"] - 1)
#
#     elif self.game.complete:
#         self.score += (self.game.time_diff * 100) if not self.completed[self.game.json["id"] - 1] else 0
#         self.completed[self.game.json["id"] - 1] = True
#         self.levelselect_buttons[self.game.json["id"] - 1].set_colors(border_color=(0, 255, 0))
#         if self.game.json["id"] + 1 > len(self.levels):
#             Constants.BIRTHDAY = True
#             self.menu_state = "main"
#         else:
#             self.start_game(self.game.json["id"])
#         self.__save_game()

