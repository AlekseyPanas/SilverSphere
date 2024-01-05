from __future__ import annotations
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from Constants import cscale
import Constants
from game.Renderers import ZHeapRenderer
from game.SpritesManager import GroupSpritesManager
from game.LevelGenerator import LevelGenerator
from Button import Button


@register_assets(ASSET_LOADER)
class GameManager(Manager):
    EXIT_ICON_IMAGE: pygame.Surface = PreAsset("assets/images/X.png", (50, 50))  # [X] icon for exiting level

    # Scaled tile size in pixels
    TILE_SIZE = cscale(50)

    # Level grid and pixel sizes
    GRID_SIZE_X = 20
    GRID_SIZE_Y = 12
    GRID_SIZE = (GRID_SIZE_X, GRID_SIZE_Y)
    GRID_PIXELS_X = TILE_SIZE * GRID_SIZE_X
    GRID_PIXELS_Y = TILE_SIZE * GRID_SIZE_Y
    GRID_PIXELS = (GRID_PIXELS_X, GRID_PIXELS_Y)

    def __init__(self, menu: Menu, level_idx: int = 23):
        super().__init__(menu)
        self.__level_json = menu.get_level_json_at_index(level_idx)  # dictionary of level object (see levels.json)
        self.__game_screen = pygame.Surface(self.GRID_PIXELS)  # surface for game
        self.__renderer = ZHeapRenderer()  # Basic renderer using heap with z-order priority
        self.__sprites_manager = GroupSpritesManager(self.__level_json)  # Stores game sprites

        self.__time = 50

        # Button
        self.__exit_button = Button(Constants.cscale(550, 640), Constants.cscale(50, 50),
                                    self.EXIT_ICON_IMAGE, state_quantity=2)

        LevelGenerator(self.__level_json).generate_sprites(self.__sprites_manager)  # Generate level
        self.__sprites_manager.flush_all()  # Flush manager. The sprites aren't added until flushed

    def run(self, screen: pygame.Surface, menu: Menu):
        # Update all sprites
        for g in self.__sprites_manager.get_all_sprites():
            for s in g:
                s.update(menu, self, self.__sprites_manager)

        self.__sprites_manager.flush_all()  # Flush manager. The sprites aren't added until flushed

        # Add content to frame and register shadows
        for g in self.__sprites_manager.get_all_sprites():
            for s in g:
                self.__renderer.add_to_frame(s.render(menu, self, self.__sprites_manager))  # Render sprite

                # Register shadows
                shad = s.get_shadow()
                if shad is not None:
                    for shadman in self.__sprites_manager.get_shadow_managers():
                        shadman.register_shadow(s)

        # Render shadows and add them
        for shadman in self.__sprites_manager.get_shadow_managers():
            self.__renderer.add_to_frame(shadman.render(menu, self, self.__sprites_manager))

        # Render frame
        self.__renderer.render_frame(self.__game_screen)

        screen.blit(self.__game_screen, (15, 15))
        self.draw_overlay(screen)

    def draw_overlay(self, screen: pygame.Surface):
        """Draws game overlay with time, level indicator, and exit button"""
        # Draw black rectangles
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(100, 640, 200, 58)), Constants.cscale(5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(300, 640, 200, 58)), Constants.cscale(5))

        # Draws time and level text
        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'TIME: ' + str(self.__time), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(200, 669)))

        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'LEVEL: ' + str(self.__level_json["id"]), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(400, 669)))

        # Draw exit button
        self.__exit_button.draw_and_hover(screen, pygame.mouse.get_pos())

    def do_persist(self) -> bool: return False

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
