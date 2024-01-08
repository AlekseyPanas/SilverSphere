from __future__ import annotations
import random
import pygame
import Button
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from managers import MenuScreenCustomManager
from Constants import path2asset, cscale
from game.LevelData import LevelData, BoxData, EnemyData
import Constants
from game.Renderers import ZHeapRenderer
from enum import IntEnum
import math
import time


class Tools(IntEnum):
    BOX = 0
    METAL = 1
    TILE = 2
    ICE = 3
    BOX_X = 4
    ICE_X = 5
    ENEMY = 6
    PLAYER = 7
    VORTEX = 8
    DELETE = 9


@register_assets(ASSET_LOADER)
class EditorManager(Manager):
    """Manager for Birthday Screen"""
    TOOL_SIZE = (60, 60)

    TOOL_BOX_IMG: pygame.Surface = PreAsset(path2asset("images/Wooden crate.png"), TOOL_SIZE)
    TOOL_METAL_IMG: pygame.Surface = PreAsset(path2asset("images/iron.png"), TOOL_SIZE)
    TOOL_TILE_IMG: pygame.Surface = PreAsset(path2asset("images/floor.png"), TOOL_SIZE)
    TOOL_ICE_IMG: pygame.Surface = PreAsset(path2asset("images/icecube.png"), TOOL_SIZE)
    TOOL_BOX_X_IMG: pygame.Surface = PreAsset(path2asset("images/Xbox.png"), TOOL_SIZE)
    TOOL_ICE_X_IMG: pygame.Surface = PreAsset(path2asset("images/Xice.png"), TOOL_SIZE)
    TOOL_ENEMY_IMG: pygame.Surface = PreAsset(path2asset("images/Golden Ball.png"), TOOL_SIZE)
    TOOL_PLAYER_IMG: pygame.Surface = PreAsset(path2asset("images/Silver Ball.png"), TOOL_SIZE)
    TOOL_VORTEX_IMG: pygame.Surface = PreAsset(path2asset("images/vortex_thumb.png"), TOOL_SIZE)
    TOOL_DELETE_IMG: pygame.Surface = PreAsset(path2asset("images/tool_delete.png"), TOOL_SIZE)

    def __init__(self, menu: Menu, custom_levels_manager: MenuScreenCustomManager.MenuScreenCustomManager, level_data_ref: LevelData):
        from game.SpritesManager import GroupSpritesManager
        from game.LevelGenerator import LevelGenerator
        from sprites import Vortex
        super().__init__(menu)

        self.__tool_assets = [self.TOOL_BOX_IMG, self.TOOL_METAL_IMG, self.TOOL_TILE_IMG, self.TOOL_ICE_IMG,
                              self.TOOL_BOX_X_IMG, self.TOOL_ICE_X_IMG, self.TOOL_ENEMY_IMG, self.TOOL_PLAYER_IMG,
                              self.TOOL_VORTEX_IMG, self.TOOL_DELETE_IMG]

        self.__selected_tool = Tools.BOX

        self.__level_data_ref = level_data_ref
        self.__custom_manager: MenuScreenCustomManager.MenuScreenCustomManager = custom_levels_manager

        self.__generate_level()

        self.__game_surf = pygame.Surface(Constants.cscale(1000, 600))

        self.__previous_grid_pos: list[tuple[int, int]] | None = None  # Used for preventing drag-deletion on same time

        self.__path_in_progress = []  # list of sequential tuple positions for current enemy being created

        self.__save_and_exit_button = Button.Button(cscale(935, 635), cscale(80, 45), None, True,
                                                    (0, 0, 0), (0, 0, 0), (150, 210, 150), ":wq", cscale(2),
                                                    Constants.get_impact(cscale(20)))

        self.__time_edit_cooldown = 0

    @staticmethod
    def __path_list_to_data(path_list: list[tuple[int, int]]) -> EnemyData:
        start_coord_xy = path_list[0]
        path_directions = []
        path_lengths = []
        index = 1
        while index < len(path_list):
            xory = 0
            porn = 0
            length = 0
            if path_list[index][0] == path_list[index - 1][0] + 1:
                path_directions.append('r')
                xory = 0
                porn = +1
            if path_list[index][0] == path_list[index - 1][0] - 1:
                path_directions.append('l')
                xory = 0
                porn = -1
            if path_list[index][1] == path_list[index - 1][1] + 1:
                path_directions.append('d')
                xory = 1
                porn = +1
            if path_list[index][1] == path_list[index - 1][1] - 1:
                path_directions.append('u')
                xory = 1
                porn = -1
            while index < len(path_list) and path_list[index][xory] == path_list[index - 1][xory] + porn:
                length = length + 1
                index = index + 1
            path_lengths.append(length)
        return EnemyData(start_coord_xy, path_directions, path_lengths)

    @staticmethod
    def __path_data_to_list(e: EnemyData) -> list[[tuple[int, int]]]:
        lst = [e.start_coord_xy]
        for i in range(len(e.path_directions)):
            d = e.path_directions[i]
            x = 0
            y = 0
            if d == 'r':
                x = +1
            if d == 'l':
                x = -1
            if d == 'd':
                y = +1
            if d == 'u':
                y = -1
            for j in range(e.path_lengths[i]):
                lst.append((lst[-1][0] + x, lst[-1][1] + y))
        return lst

    def __generate_level(self):
        from game.SpritesManager import GroupSpritesManager
        from game.LevelGenerator import LevelGenerator
        from sprites import Vortex
        from sprites.Player import Player
        self.__renderer = ZHeapRenderer()
        self.__sprite_manager = GroupSpritesManager(self.__level_data_ref.to_dict(), self.__renderer)
        self.__level_generator: LevelGenerator = LevelGenerator(self.__level_data_ref.to_dict())
        self.__level_generator.generate_sprites(self.__sprite_manager)
        self.__sprite_manager.flush_all()

        self.__vortex = self.__sprite_manager.get_single(Vortex.Vortex)
        self.__vortex.state = "stationary"
        self.__vortex.current_image = self.__vortex.stationary
        self.__vortex.current_index = 0

        self.__player = self.__sprite_manager.get_single(Player)

    def __has_water(self, grid_coords: tuple[int, int]) -> bool:
        return self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] == "W"

    def __has_metal(self, grid_coords: tuple[int, int]) -> bool:
        return self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] == "B"

    def __has_tile(self, grid_coords: tuple[int, int]) -> bool:
        return self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] == "T"

    def __has_box_or_ice(self, grid_coords: tuple[int, int]) -> bool:
        for b in self.__level_data_ref.boxes:
            if b.coord_xy[0] == grid_coords[0] and b.coord_xy[1] == grid_coords[1]:
                return True
        return False

    def __has_player_or_enemy(self, grid_coords: tuple[int, int]) -> bool:
        ply = self.__level_data_ref.player_start_coord_xy
        if ply[0] == grid_coords[0] and ply[1] == grid_coords[1]: return True
        for e in self.__level_data_ref.enemies:
            if e.start_coord_xy[0] == grid_coords[0] and e.start_coord_xy[1] == grid_coords[1]:
                return True
        return False

    def __has_enemy(self, grid_coords: tuple[int, int]) -> bool:
        for e in self.__level_data_ref.enemies:
            if e.start_coord_xy[0] == grid_coords[0] and e.start_coord_xy[1] == grid_coords[1]:
                return True
        return False

    def __get_enemy(self, grid_coords: tuple[int, int]) -> EnemyData | None:
        for e in self.__level_data_ref.enemies:
            if e.start_coord_xy[0] == grid_coords[0] and e.start_coord_xy[1] == grid_coords[1]:
                return e
        return None

    def __has_x(self, grid_coords: tuple[int, int]) -> bool:
        for x in self.__level_data_ref.ice_x_coords_xy + self.__level_data_ref.box_x_coords_xy:
            if x[0] == grid_coords[0] and x[1] == grid_coords[1]:
                return True
        return False

    def __has_vortex(self, grid_coords: tuple[int, int]) -> bool:
        return self.__level_data_ref.vortex_coord_xy[0] == grid_coords[0] and \
            self.__level_data_ref.vortex_coord_xy[1] == grid_coords[1]

    def __is_completely_clear_tile(self, grid_coords: tuple[int, int]) -> bool:
        return self.__is_box_placeable(grid_coords) and not self.__has_x(grid_coords)

    def __is_box_placeable(self, grid_coords: tuple[int, int]) -> bool:
        return self.__has_tile(grid_coords) and not self.__has_box_or_ice(grid_coords) and \
            not self.__has_player_or_enemy(grid_coords) and not self.__has_vortex(grid_coords)

    def __is_x_placeable(self, grid_coords: tuple[int, int]) -> bool:
        return self.__is_completely_clear_tile(grid_coords) or \
            (self.__has_player_or_enemy(grid_coords) and (not self.__has_x(grid_coords))) or \
            (self.__has_box_or_ice(grid_coords) and (not self.__has_x(grid_coords)))

    @staticmethod
    def __coords_from_pixels(pixel_pos: tuple[int, int]):
        return (pixel_pos[0] - cscale(15)) // cscale(50), (pixel_pos[1] - cscale(15)) // cscale(50)

    def run(self, screen: pygame.Surface, menu: Menu):
        from sprites.Sprite import Sprite, ZHeights
        from sprites.Box import Box, IceCube
        from sprites.X import X_Ice_Tile, X_Box_Tile
        from sprites.Enemy import Enemy
        self.__sprite_manager.render_level(menu, self.__game_surf)
        screen.blit(self.__game_surf, Constants.cscale(15, 15))
        self.__draw_toolbar(screen)

        if pygame.mouse.get_pressed()[0]:
            msps = pygame.mouse.get_pos()
            grid_coords = self.__coords_from_pixels(msps)
            scaled_pos = Sprite.get_center_from_coords(grid_coords)

            if (0 <= grid_coords[0] < Constants.GRID_DIMS[0]) and (0 <= grid_coords[1] < Constants.GRID_DIMS[1]) and \
                    grid_coords != self.__previous_grid_pos:

                match self.__selected_tool:
                    case Tools.BOX:
                        if self.__is_box_placeable(grid_coords):
                            self.__level_data_ref.boxes.append(BoxData(grid_coords, False))
                            self.__sprite_manager.add_sprite(Box(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, grid_coords))
                            self.__sprite_manager.flush_all()
                    case Tools.ICE:
                        if self.__is_box_placeable(grid_coords):
                            self.__level_data_ref.boxes.append(BoxData(grid_coords, True))
                            self.__sprite_manager.add_sprite(
                                IceCube(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, grid_coords))
                            self.__sprite_manager.flush_all()
                    case Tools.TILE:
                        if self.__has_water(grid_coords) or self.__has_metal(grid_coords):
                            self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] = "T"
                            self.__generate_level()
                    case Tools.METAL:
                        if self.__has_water(grid_coords) or self.__is_completely_clear_tile(grid_coords):
                            self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] = "B"
                            self.__generate_level()
                    case Tools.VORTEX:
                        if self.__is_completely_clear_tile(grid_coords):
                            self.__vortex.pos = scaled_pos
                            self.__level_data_ref.vortex_coord_xy = grid_coords
                    case Tools.PLAYER:
                        if self.__is_box_placeable(grid_coords):
                            self.__level_data_ref.player_start_coord_xy = grid_coords
                            self.__player.pos = Sprite.get_center_from_coords(grid_coords)
                    case Tools.BOX_X:
                        if self.__is_x_placeable(grid_coords):
                            self.__level_data_ref.box_x_coords_xy.append(grid_coords)
                            self.__sprite_manager.add_sprite(X_Box_Tile(None, ZHeights.X_HEIGHT, grid_coords))
                            self.__sprite_manager.flush_all()
                    case Tools.ICE_X:
                        if self.__is_x_placeable(grid_coords):
                            self.__level_data_ref.ice_x_coords_xy.append(grid_coords)
                            self.__sprite_manager.add_sprite(X_Ice_Tile(None, ZHeights.X_HEIGHT, grid_coords))
                            self.__sprite_manager.flush_all()
                    case Tools.DELETE:
                        if self.__has_x(grid_coords):
                            self.__level_data_ref.box_x_coords_xy = [
                                x for x in self.__level_data_ref.box_x_coords_xy if
                                x[0] != grid_coords[0] or x[1] != grid_coords[1]]
                            self.__level_data_ref.ice_x_coords_xy = [
                                x for x in self.__level_data_ref.ice_x_coords_xy if
                                x[0] != grid_coords[0] or x[1] != grid_coords[1]]
                        elif self.__has_box_or_ice(grid_coords):
                            self.__level_data_ref.boxes = [
                                b for b in self.__level_data_ref.boxes if
                                b.coord_xy[0] != grid_coords[0] or b.coord_xy[1] != grid_coords[1]]
                        elif self.__has_tile(grid_coords) and self.__is_completely_clear_tile(grid_coords):
                            self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] = 'W'
                        elif self.__has_metal(grid_coords):
                            self.__level_data_ref.layout[grid_coords[1]][grid_coords[0]] = 'W'
                        elif self.__has_enemy(grid_coords):
                            self.__level_data_ref.enemies = [
                                e for e in self.__level_data_ref.enemies if
                                e.start_coord_xy[0] != grid_coords[0] or e.start_coord_xy[1] != grid_coords[1]]
                        self.__generate_level()
                    case Tools.ENEMY:
                        last = (-1, -1) if not len(self.__path_in_progress) else self.__path_in_progress[-1]
                        if grid_coords[0] != last[0] or grid_coords[1] != last[1]:  # Not same tile as end of path
                            if (not len(self.__path_in_progress) or
                                    (abs(grid_coords[0] - last[0]) <= 1 and grid_coords[1] - last[1] == 0) or
                                    (abs(grid_coords[1] - last[1]) <= 1 and grid_coords[0] - last[0] == 0)) and \
                                    (not self.__has_metal(grid_coords) and not self.__has_vortex(grid_coords)):
                                self.__path_in_progress.append(tuple(grid_coords))
                    case _:
                        print("YOU SHOULDN'T BE HERE")

                self.__previous_grid_pos = grid_coords
        else:  # Mouse unpressed
            if len(self.__path_in_progress) and self.__path_in_progress[0] == self.__path_in_progress[-1]:
                self.__level_data_ref.enemies.append(self.__path_list_to_data(self.__path_in_progress))
                self.__sprite_manager.add_sprite(
                    Enemy(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, self.__path_in_progress[0], ["u"], [5]))
                self.__sprite_manager.flush_all()
            self.__path_in_progress = []

        for e in menu.events:
            if e.type == pygame.KEYUP:
                if e.unicode in [str(i) for i in range(0, len(Tools) + 1)]:
                    new_tool = int(e.unicode)
                    if new_tool == 0: new_tool = Tools(9)
                    else: new_tool = Tools(int(e.unicode) - 1)

                    if new_tool.value != self.__selected_tool.value:
                        self.__selected_tool = new_tool
                        self.__previous_grid_pos = None
                        self.__path_in_progress = []

        # Draw semi-transparent path for all enemies (except selected)
        ms_coords = self.__coords_from_pixels(pygame.mouse.get_pos())
        for e in self.__level_data_ref.enemies:
            op = 50
            if e.start_coord_xy[0] == ms_coords[0] and e.start_coord_xy[1] == ms_coords[1]:
                op = 180
            self.__draw_path(screen, self.__path_data_to_list(e), opacity=op)

        # Draw path in progress
        if len(self.__path_in_progress):
            self.__draw_path(screen, self.__path_in_progress, (0, 255, 0), 200)

        # Render button and events
        self.__save_and_exit_button.draw_and_hover(screen, pygame.mouse.get_pos())
        for e in menu.events:
            if e.type == pygame.MOUSEBUTTONUP:
                if self.__save_and_exit_button.is_clicked(e.pos):
                    self.__custom_manager.save_levels()
                    menu.switch_state(Menu.MenuStates.CUSTOMLEVELSEL)

        # Time text
        time_title = Constants.get_arial(cscale(25)).render("Time:", True, (255, 255, 255))
        time_text = Constants.get_arial(cscale(35)).render(str(self.__level_data_ref.time_limit), True, (255, 255, 255))
        screen.blit(time_title, time_title.get_rect(center=(cscale(870, 635))))
        screen.blit(time_text, time_text.get_rect(center=(cscale(870, 665))))

        # Time editing
        COOLDOWN = 3
        if pygame.key.get_pressed()[pygame.K_UP] and self.__time_edit_cooldown == 0:
            self.__level_data_ref.time_limit += 1
            self.__time_edit_cooldown = COOLDOWN
        elif pygame.key.get_pressed()[pygame.K_DOWN] and self.__time_edit_cooldown == 0 and self.__level_data_ref.time_limit > 1:
            self.__level_data_ref.time_limit -= 1
            self.__time_edit_cooldown = COOLDOWN
        self.__time_edit_cooldown = max(0, self.__time_edit_cooldown - 1)


    def __draw_path(self, screen: pygame.Surface, path: list[tuple[int, int]], color=(255, 0, 0), opacity=255):
        """Draws moving dotted path using unix time based on given coordinates"""
        from sprites.Sprite import Sprite

        ms_per_tile = 800  # Time to move across a single tile
        dots_per_tile = 3
        num_dots = len(path) * dots_per_tile
        time_shift = ms_per_tile / dots_per_tile

        def get_pos_from_time(cur_time: float) -> tuple[int, int] | None:
            non_modded_idx = cur_time // ms_per_tile
            idx_cur = int(non_modded_idx % len(path))
            idx_next = int((idx_cur + 1) % len(path))

            if idx_next == 0: return None

            interp = (cur_time - (non_modded_idx * ms_per_tile)) / ms_per_tile

            pos_x = path[idx_cur][0] + (path[idx_next][0] - path[idx_cur][0]) * interp
            pox_y = path[idx_cur][1] + (path[idx_next][1] - path[idx_cur][1]) * interp

            pos = cscale(*Sprite.get_center_from_coords((pos_x, pox_y)))
            pos = (pos[0] + cscale(15), pos[1] + cscale(15))
            return pos

        t = time.time() * 1000
        for i in range(num_dots):
            p = get_pos_from_time(t)
            if p is not None:
                surf = pygame.Surface(cscale(10, 10), pygame.SRCALPHA, 32)
                pygame.draw.circle(surf, color, cscale(5, 5), cscale(5))
                surf.fill((0, 0, 0, 255 - opacity), special_flags=pygame.BLEND_RGBA_SUB)
                screen.blit(surf, surf.get_rect(center=p))
            t += time_shift

    def __draw_toolbar(self, screen: pygame.Surface):
        for i in range(len(Tools)):
            screen.blit(self.__tool_assets[i], Constants.cscale(i * 80 + 25, 630))
        pygame.draw.rect(screen, (255, 255, 255), Constants.cscale(self.__selected_tool * 80 + 20, 625, 70, 70), Constants.cscale(4), )

    def do_persist(self) -> bool: return False
