from __future__ import annotations
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
import Constants
from Constants import cscale


@register_assets(ASSET_LOADER)
class GameManager(Manager):
    # Scaled tile size in pixels
    TILE_SIZE = cscale(50)

    # Level grid and pixel sizes
    GRID_SIZE_X = 20
    GRID_SIZE_Y = 12
    GRID_SIZE = (GRID_SIZE_X, GRID_SIZE_Y)
    GRID_PIXELS_X = TILE_SIZE * GRID_SIZE_X
    GRID_PIXELS_Y = TILE_SIZE * GRID_SIZE_Y
    GRID_PIXELS = (GRID_PIXELS_X, GRID_PIXELS_Y)

    def __init__(self, menu: Menu, level_idx: int = 0):
        super().__init__(menu)
        self.level_json = menu.get_level_json_at_index(level_idx)

        self.game_screen = pygame.Surface(self.GRID_PIXELS)

    def run(self, screen: pygame.Surface, menu: Menu):
        # Draw Marble
        screen.blit(self.MARBLE_IMAGE, Constants.cscale(15, 15))

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
