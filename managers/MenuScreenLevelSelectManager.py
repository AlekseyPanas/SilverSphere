from __future__ import annotations
import pygame
from managers.Managers import ASSET_LOADER, register_assets, PreAsset
from managers.MenuScreenManager import MenuScreenManager
import Menu
import Button
import Constants
from Constants import path2asset


@register_assets(ASSET_LOADER)
class MenuScreenLevelSelectManager(MenuScreenManager):
    LOCK_IMAGE: pygame.Surface = PreAsset(path2asset("images/lock_icon.png"), (50, 50))

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
            if menu.completed[idx]:
                button.set_colors(border_color=(0, 255, 0))
            button.draw(screen)
            button.is_hover(pygame.mouse.get_pos())
            if not idx == 0:
                if not menu.completed[idx - 1]:
                    screen.blit(self.LOCK_IMAGE, self.LOCK_IMAGE.get_rect(center=button.button_rect.center))

        for event in menu.events:
            for idx, button in enumerate(self.levelselect_buttons):
                # Checks for presses on buttons
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.is_clicked(event.pos):
                        if idx == 0 or menu.completed[idx - 1]:
                            menu.switch_state(Menu.MenuStates.GAME, {"level_idx": idx})

            if event.type == pygame.MOUSEBUTTONUP:
                if self.back_button.is_clicked(event.pos):
                    menu.switch_state(Menu.MenuStates.MAIN)
