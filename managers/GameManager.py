from __future__ import annotations
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from Constants import cscale, path2asset
import Constants
from game.Renderers import ZHeapRenderer
from game.SpritesManager import GroupSpritesManager
from game.LevelGenerator import LevelGenerator
from Button import Button
from sprites.Vortex import Vortex
from sprites.X import X_Ice_Tile, X_Box_Tile
from sprites.Box import Box, IceCube
from sprites.Player import Player
from sprites.AnimationEffect import ExplosionAnimation
import copy
import time
from enum import IntEnum


class GameStates(IntEnum):
    NOT_STARTED = 0
    IN_GAME = 1
    WON = 2


@register_assets(ASSET_LOADER)
class GameManager(Manager):
    EXIT_ICON_IMAGE: pygame.Surface = PreAsset(path2asset("images/X.png"), (50, 50))  # [X] icon for exiting level
    INLEVEL_PLAY_BUTTON_IMAGE: pygame.Surface = PreAsset(path2asset("images/play.png"))
    NEXTLVL_BUTTON_IMAGE: pygame.Surface = PreAsset(path2asset("images/nxtlvl.png"))

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
        # JSON level data
        self.__level_json = menu.get_level_json_at_index(level_idx)  # dictionary of level object (see levels.json)
        self.__layout = copy.deepcopy(self.__level_json["layout"])

        # Core game objects
        self.__game_screen = pygame.Surface(self.GRID_PIXELS)  # surface for game
        self.__renderer = ZHeapRenderer()  # Basic renderer using heap with z-order priority
        self.__sprites_manager = GroupSpritesManager(self.__level_json)  # Stores game sprites

        # Game state tracking
        self.__start_time = -1
        self.__time_left = self.__level_json["time"]
        self.__state = GameStates.NOT_STARTED
        self.__explosion_generated = False  # Flag to spawn explosion when time runs out

        # Asset generation
        self.__exit_button = Button(Constants.cscale(550, 640), Constants.cscale(50, 50), self.EXIT_ICON_IMAGE, state_quantity=2)
        self.__play_button = Button(Constants.cscale(425, 440), Constants.cscale(180, 60), self.INLEVEL_PLAY_BUTTON_IMAGE, state_quantity=2)
        self.__next_level_button = Button(Constants.cscale(55, 480), Constants.cscale(180, 60), self.NEXTLVL_BUTTON_IMAGE, state_quantity=2)
        self.__pre_level_popup_surf = self.__generate_pre_popup()
        self.__post_level_popup_surf = self.__generate_post_popup()

        # Initialize level
        LevelGenerator(self.__level_json).generate_sprites(self.__sprites_manager)  # Generate level
        self.__sprites_manager.flush_all()  # Flush manager. The sprites aren't added until flushed

        # Useful references for quick access
        self.player: Player = self.__sprites_manager.get_single(Player)
        self.vortex: Vortex = self.__sprites_manager.get_single(Vortex)

    def get_layout(self) -> list[list[str]]:
        """Return level's string-based layout"""
        return self.__layout

    def set_layout_solid_at(self, row: int, col: int):
        """Creates a solid tile with no visual. This is for when boxes fall into water"""
        self.__layout[row][col] = "S"

    def run(self, screen: pygame.Surface, menu: Menu.Menu):
        # Button events
        for event in menu.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.__exit_button.is_clicked(event.pos):
                    menu.switch_state(Menu.MenuStates.MAIN)
                elif self.__state == GameStates.NOT_STARTED and self.__play_button.is_clicked(event.pos):
                    self.__state = GameStates.IN_GAME
                    self.__start_time = copy.copy(time.time())
                elif self.__state == GameStates.WON and self.__next_level_button.is_clicked(event.pos):
                    pass

        if self.__state == GameStates.IN_GAME:

            # Update all sprites
            for s in self.__sprites_manager.get_all_sprites():
                s.update(menu, self, self.__sprites_manager)

            # Run level logic
            self.__run_level_logic(menu)

        # Flush manager. The sprites aren't added until flushed
        self.__sprites_manager.flush_all()

        # Drawing
        self.__render_level(menu)
        screen.blit(self.__game_screen, (15, 15))
        self.__draw_overlay(screen)

        if self.__state == GameStates.NOT_STARTED:
            screen.blit(self.__pre_level_popup_surf, self.__pre_level_popup_surf.get_rect(center=(Constants.SCREEN_SIZE[0] / 2, Constants.SCREEN_SIZE[1] / 2)))
            self.__play_button.draw_and_hover(screen, pygame.mouse.get_pos())
        elif self.__state == GameStates.WON:
            screen.blit(self.__post_level_popup_surf, self.__post_level_popup_surf.get_rect(center=(Constants.SCREEN_SIZE[0] / 2, Constants.SCREEN_SIZE[1] / 2)))
            self.__next_level_button.draw_and_hover(screen, pygame.mouse.get_pos())

    def __render_level(self, menu: Menu.Menu):
        """Render every sprite and push to renderer class. Then render whole frame onto game screen"""
        # #################################################### Potentially extract and remove some params from render method
        # Add content to frame and register shadows
        for s in self.__sprites_manager.get_all_sprites():
            render_output = s.render(menu, self, self.__sprites_manager)
            if render_output is not None:
                self.__renderer.add_to_frame(render_output)  # Render sprite

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
        ###########################################################

    def __draw_overlay(self, screen: pygame.Surface):
        """Draws game overlay with time, level indicator, and exit button"""
        # Draw black rectangles
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(100, 640, 200, 58)), Constants.cscale(5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(300, 640, 200, 58)), Constants.cscale(5))

        # Draws time and level text
        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'TIME: ' + str(self.__time_left), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(200, 669)))

        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'LEVEL: ' + str(self.__level_json["id"]), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(400, 669)))

        # Draw exit button
        self.__exit_button.draw_and_hover(screen, pygame.mouse.get_pos())

    def do_persist(self) -> bool: return False

    def __run_level_logic(self, menu: Menu.Menu):
        """Core level logic for sprites, not including menus"""
        # Counts timer and resets game if time runs out
        time_current = time.time()
        self.__time_left = self.__level_json["time"] - int(time_current - self.__start_time)

        if self.__time_left <= 0:
            self.player.kill = True
            if not self.__explosion_generated:
                self.__sprites_manager.add_sprite(ExplosionAnimation(self.player.pos))
            self.__explosion_generated = True

        # Detects if all X marks are satisfied. open_exit initially set to false
        self.open_exit = False
        # temporary array to report the status of each x mark
        x_satisfaction = True
        # If there are no Xs, exit opens automatically
        x_ice_tiles = self.__sprites_manager.get_group(X_Ice_Tile)
        x_box_tiles = self.__sprites_manager.get_group(X_Box_Tile)
        if not len(x_ice_tiles) and not len(x_box_tiles):
            self.open_exit = True
        else:
            # Checks if any X's aren't satisfied
            for x in x_ice_tiles:
                satisfied = False
                for box in self.__sprites_manager.get_group(IceCube):
                    if box.coords == x.coords:
                        satisfied = True
                if not satisfied:
                    x_satisfaction = False

            for x in x_box_tiles:
                satisfied = False
                for box in self.__sprites_manager.get_groups([IceCube, Box]):
                    if box.coords == x.coords:
                        satisfied = True
                if not satisfied:
                    x_satisfaction = False

            # If all Xs are satisfied, exit opens
            if x_satisfaction:
                self.open_exit = True

        # controls animations with vortex
        vortex: Vortex = self.__sprites_manager.get_single(Vortex)
        if self.open_exit and vortex.state == 'blank':
            vortex.set_image = False
            vortex.state = 'open'
        elif not self.open_exit and vortex.state == 'stationary':
            vortex.set_image = False
            vortex.state = 'close'

    def __generate_pre_popup(self) -> pygame.Surface:
        # LOADS POPUP FOR PRE LEVEL
        pre_level_popup_surf = pygame.Surface((430, 350))
        pre_level_popup_surf.fill((0, 0, 0))
        pygame.draw.rect(pre_level_popup_surf, (205, 175, 149), pygame.Rect(3, 3, 424, 344))

        rendered_text = Constants.get_arial(Constants.cscale(50, divisors=(1030,))).render('~*SILVERBALL*~', True,
                                                                                           (0, 0, 0))
        pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 40)))

        rendered_text = Constants.get_arial(Constants.cscale(25, divisors=(1030,))).render(
            'LEVEL:' + str(self.__level_json["id"]), True, (0, 0, 0))
        pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 80)))

        rendered_text = Constants.get_arial(Constants.cscale(30, divisors=(1030,))).render('NAME', True, (0, 0, 0))
        pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 160)))

        rendered_text = Constants.get_arial(Constants.cscale(30, divisors=(1030,))).render('_____', True, (0, 0, 0))
        pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 165)))

        rendered_text = Constants.get_arial(Constants.cscale(35, divisors=(1030,))).render(self.__level_json["name"], True,
                                                                                           (0, 0, 0))
        pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 210)))

        return pygame.transform.smoothscale(pre_level_popup_surf, Constants.cscale(430, 350)).convert_alpha()

    def __generate_post_popup(self) -> pygame.Surface:
        # POST LEVEL
        post_level_popup_surf = pygame.Surface((250, 450))
        post_level_popup_surf.fill((0, 0, 0))
        pygame.draw.rect(post_level_popup_surf, (205, 175, 149), pygame.Rect(3, 3, 244, 444))

        rendered_text = Constants.get_arial(Constants.cscale(40, divisors=(1030,))).render(
            'LEVEL ' + str(self.__level_json["id"]), True, (0, 0, 0))
        post_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(125, 40)))

        rendered_text = Constants.get_arial(Constants.cscale(40, divisors=(1030,))).render('COMPLETE!!', True,
                                                                                           (0, 0, 0))
        post_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(125, 80)))

        rendered_text = Constants.get_sans(Constants.cscale(38, divisors=(1030,))).render('SCORE:', True, (0, 0, 0))
        post_level_popup_surf.blit(rendered_text, (15, 160))

        rendered_text = Constants.get_sans(Constants.cscale(38, divisors=(1030,))).render('TOTAL SCORE:', True,
                                                                                          (0, 0, 0))
        post_level_popup_surf.blit(rendered_text, (15, 270))

        return pygame.transform.smoothscale(post_level_popup_surf, Constants.cscale(250, 450)).convert_alpha()

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

# Draws post-level menu
# screen.blit(self.post_level_popup_surf, self.post_level_popup_surf.get_rect(
#     center=Constants.cscale(160, 330)))
#
# score_gain = self.time_diff * 100 if not Globe.MENU.completed[self.json["id"] - 1] else 0
#
# rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(score_gain), True, (0, 0, 0))
# self.post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 190))
#
# rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(Globe.MENU.score + score_gain), True, (0, 0, 0))
# self.post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 300))
#
# self.next_level_button.draw(screen)
# self.next_level_button.is_hover(pygame.mouse.get_pos())
# for event in Globe.events:
#     if event.type == pygame.MOUSEBUTTONUP:
#         if self.next_level_button.is_clicked(event.pos):
#             self.complete = True
