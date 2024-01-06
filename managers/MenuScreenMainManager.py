from __future__ import annotations
import pygame
from managers.Managers import ASSET_LOADER, register_assets, PreAsset
from managers.MenuScreenManager import MenuScreenManager
import Menu
import Button
import Constants
from Constants import path2asset


@register_assets(ASSET_LOADER)
class MenuScreenMainManager(MenuScreenManager):
    PLAY_BUTTON: pygame.Surface = PreAsset(path2asset("menu_play_button.png"))
    LEVEL_BUTTON: pygame.Surface = PreAsset(path2asset("menu_levels_button.png"))
    QUIT_BUTTON: pygame.Surface = PreAsset(path2asset("menu_quit_button.png"))
    BUTTON_SIZE = (200, 67)

    def __init__(self, menu: Menu):
        super().__init__(menu)
        # Instantiate Play button and other buttons
        self.play_button = Button.Button(Constants.cscale(150, 205), Constants.cscale(*self.BUTTON_SIZE),
                                         self.PLAY_BUTTON, state_quantity=2)
        self.level_select_button = Button.Button(Constants.cscale(150, 295), Constants.cscale(*self.BUTTON_SIZE),
                                                 self.LEVEL_BUTTON, state_quantity=2)
        self.quit_button = Button.Button(Constants.cscale(150, 385), Constants.cscale(*self.BUTTON_SIZE),
                                         self.QUIT_BUTTON, state_quantity=2)

    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        # Render buttons
        self.play_button.draw_and_hover(screen, pygame.mouse.get_pos())
        self.level_select_button.draw_and_hover(screen, pygame.mouse.get_pos())
        self.quit_button.draw_and_hover(screen, pygame.mouse.get_pos())

        # Draws score
        rendered_text = Constants.get_impact(Constants.cscale(35)).render("Score: " + str(menu.score), False, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(750, 250)))

        # Menu Button events
        for event in menu.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_button.is_clicked(event.pos):
                    # Takes you to the next uncompleted level
                    for idx in range(len(menu.completed)):
                        if not menu.completed[idx]:
                            menu.switch_state(Menu.MenuStates.GAME, {"level_idx": idx})
                            break

                elif self.level_select_button.is_clicked(event.pos):
                    menu.switch_state(Menu.MenuStates.LEVELSEL)

                elif self.quit_button.is_clicked(event.pos):
                    menu.stop_game()
