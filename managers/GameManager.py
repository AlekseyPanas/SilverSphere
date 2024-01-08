from __future__ import annotations
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from Constants import cscale, path2asset
import Constants
from game.Renderers import ZHeapRenderer
from game import SpritesManager
from game import LevelGenerator
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

    TICKS_UNTIL_RESET = 50

    def __init__(self, menu: Menu, level_json: dict, level_idx: int | None = None):
        super().__init__(menu)
        # JSON level data
        self.__level_idx: int | None = level_idx  # None if custom
        self.__level_json = level_json  # dictionary of level object (see levels.json)
        self.__layout = copy.deepcopy(self.__level_json["layout"])

        # Core game objects
        self.__game_screen = pygame.Surface(self.GRID_PIXELS)  # surface for game
        self.__renderer = ZHeapRenderer()  # Basic renderer using heap with z-order priority
        self.__sprites_manager = SpritesManager.GroupSpritesManager(self.__level_json, self.__renderer)  # Stores game sprites

        # Game state tracking
        self.__start_time = -1
        self.__time_left = self.__level_json["time"]
        self.__state = GameStates.NOT_STARTED
        self.__explosion_generated = False  # Flag to spawn explosion when time runs out
        self.__gameover = False  # Flag set to indicate level was lost
        self.__reset_timer = 0  # Tick-based timer used to reset the level after loss
        self.__score_gain = 0  # Store score gain after completing level

        # Asset generation
        self.__exit_button = Button(Constants.cscale(550, 640), Constants.cscale(50, 50), self.EXIT_ICON_IMAGE, state_quantity=2)
        self.__play_button = Button(Constants.cscale(425, 440), Constants.cscale(180, 60), self.INLEVEL_PLAY_BUTTON_IMAGE, state_quantity=2)
        self.__next_level_button = Button(Constants.cscale(80, 480), Constants.cscale(180, 60), self.NEXTLVL_BUTTON_IMAGE, state_quantity=2)
        self.__pre_level_popup_surf = self.__generate_pre_popup()
        self.__post_level_popup_surf = self.__generate_post_popup()

        # Initialize level
        LevelGenerator.LevelGenerator(self.__level_json).generate_sprites(self.__sprites_manager)  # Generate level
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
        # Level reset timer
        if self.__gameover:
            self.__reset_timer += 1
        if self.__reset_timer > self.TICKS_UNTIL_RESET:
            menu.switch_state(Menu.MenuStates.GAME, {"level_json": self.__level_json, "level_idx": self.__level_idx})

        # Button events
        for event in menu.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.__exit_button.is_clicked(event.pos):
                    menu.switch_state(Menu.MenuStates.MAIN)

                elif self.__state == GameStates.NOT_STARTED and self.__play_button.is_clicked(event.pos):
                    self.__state = GameStates.IN_GAME
                    self.__start_time = copy.copy(time.time())

                elif self.__state == GameStates.WON and self.__next_level_button.is_clicked(event.pos):
                    if self.__level_idx is not None:
                        menu.score += self.__score_gain
                        menu.completed[self.__level_json["id"] - 1] = True
                    if self.__level_idx is None:
                        menu.switch_state(Menu.MenuStates.CUSTOMLEVELSEL)
                    elif self.__level_json["id"] + 1 > len(menu.levels):
                        menu.switch_state(Menu.MenuStates.MAIN)
                    else:
                        menu.switch_state(Menu.MenuStates.GAME, {"level_json": menu.get_level_json_at_index(self.__level_idx + 1), "level_idx": self.__level_idx + 1})
                    menu.save_game()

        if self.__state == GameStates.IN_GAME:
            # Update all sprites
            for s in self.__sprites_manager.get_all_sprites():
                s.update(menu, self, self.__sprites_manager)

            # Run level logic
            if not self.__gameover and not self.vortex.player_in:
                self.__level_time_and_death_logic()
            self.__level_vortex_condition_logic(menu)

        # Flush manager. The sprites aren't added until flushed
        self.__sprites_manager.flush_all()

        # Drawing
        self.__sprites_manager.render_level(menu, self.__game_screen)
        screen.blit(self.__game_screen, cscale(15, 15))
        self.__draw_overlay(screen)

        if self.__state == GameStates.NOT_STARTED:
            screen.blit(self.__pre_level_popup_surf, self.__pre_level_popup_surf.get_rect(center=(Constants.SCREEN_SIZE[0] / 2, Constants.SCREEN_SIZE[1] / 2)))
            self.__play_button.draw_and_hover(screen, pygame.mouse.get_pos())
        elif self.__state == GameStates.WON:
            screen.blit(self.__post_level_popup_surf, self.__post_level_popup_surf.get_rect(center=(Constants.SCREEN_SIZE[0] / 6.05, Constants.SCREEN_SIZE[1] / 2)))
            self.__next_level_button.draw_and_hover(screen, pygame.mouse.get_pos())

            rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(self.__score_gain), True, (0, 0, 0))
            self.__post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 190))

            rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(menu.score + self.__score_gain), True, (0, 0, 0))
            self.__post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 300))

    def __draw_overlay(self, screen: pygame.Surface):
        """Draws game overlay with time, level indicator, and exit button"""
        # Draw black rectangles
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(100, 640, 200, 58)), Constants.cscale(5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(300, 640, 200, 58)), Constants.cscale(5))

        # Draws time and level text
        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'TIME: ' + str(self.__time_left), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(200, 669)))

        level_text = "C" if self.__level_json["id"] == "CUSTOM" else str(self.__level_json["id"])
        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render(
            'LEVEL: ' + level_text, True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(400, 669)))

        # Draw exit button
        self.__exit_button.draw_and_hover(screen, pygame.mouse.get_pos())

    def do_persist(self) -> bool: return False

    def __level_time_and_death_logic(self):
        """Core level logic for sprites, not including menus"""
        # Counts timer and resets game if time runs out
        time_current = time.time()
        self.__time_left = self.__level_json["time"] - int(time_current - self.__start_time)

        if self.__time_left <= 0:
            self.player.kill = True
            if not self.__explosion_generated:
                self.__sprites_manager.add_sprite(ExplosionAnimation(self.player.pos))
                self.__explosion_generated = True

        if self.player.state == "drown" or (self.player.kill and (not self.vortex.player_in)):
            self.__gameover = True

    def __level_vortex_condition_logic(self, menu: Menu.Menu):
        """Determines if the level satisfies the conditions for the vortex to be opened"""
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
        if self.open_exit and vortex.state == 'blank' and (not vortex.player_in):
            vortex.set_image = False
            vortex.state = 'open'
        elif not self.open_exit and vortex.state == 'stationary':
            vortex.set_image = False
            vortex.state = 'close'

        if vortex.player_in and vortex.state == "blank":
            self.__state = GameStates.WON
            if self.__level_idx is not None:
                self.__score_gain = (self.__time_left * 100) if not menu.completed[self.__level_json["id"] - 1] else 0

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
