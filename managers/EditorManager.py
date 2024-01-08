from __future__ import annotations
import random
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from managers import MenuScreenCustomManager
from Constants import path2asset
from game.LevelData import LevelData, BoxData, EnemyData
import Constants
from game.Renderers import ZHeapRenderer
from enum import IntEnum


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
    TOOL_SIZE = (70, 70)

    TOOL_BOX_IMG: pygame.Surface = PreAsset(path2asset("images/Wooden crate.png"), TOOL_SIZE)
    TOOL_METAL_IMG: pygame.Surface = PreAsset(path2asset("images/iron.png"), TOOL_SIZE)
    TOOL_TILE_IMG: pygame.Surface = PreAsset(path2asset("images/floor.png"), TOOL_SIZE)
    TOOL_ICE_IMG: pygame.Surface = PreAsset(path2asset("images/icecube.png"), TOOL_SIZE)
    TOOL_BOX_X_IMG: pygame.Surface = PreAsset(path2asset("images/Xbox.png"), TOOL_SIZE)
    TOOL_ICE_X_IMG: pygame.Surface = PreAsset(path2asset("images/Xice.png"), TOOL_SIZE)
    TOOL_ENEMY_IMG: pygame.Surface = PreAsset(path2asset("images/Golden Ball.png"), TOOL_SIZE)
    TOOL_PLAYER_IMG: pygame.Surface = PreAsset(path2asset("images/Silver Ball.png"), TOOL_SIZE)
    TOOL_VORTEX_IMG: pygame.Surface = PreAsset(path2asset("images/vortex_thumb.png"), TOOL_SIZE)
    TOOL_DELETE_IMG: pygame.Surface = PreAsset(path2asset("images/floor.png"), TOOL_SIZE)

    def __init__(self, menu: Menu, custom_levels_manager: MenuScreenCustomManager, level_data_ref: LevelData):
        from game.SpritesManager import GroupSpritesManager
        from game.LevelGenerator import LevelGenerator
        from sprites import Vortex
        super().__init__(menu)

        self.__tool_assets = [self.TOOL_BOX_IMG, self.TOOL_METAL_IMG, self.TOOL_TILE_IMG, self.TOOL_ICE_IMG,
                              self.TOOL_BOX_X_IMG, self.TOOL_ICE_X_IMG, self.TOOL_ENEMY_IMG, self.TOOL_PLAYER_IMG,
                              self.TOOL_VORTEX_IMG, self.TOOL_DELETE_IMG]

        self.__level_data_ref = level_data_ref
        self.__custom_manager = custom_levels_manager

        self.__renderer = ZHeapRenderer()
        self.__sprite_manager = GroupSpritesManager(level_data_ref.to_dict(), self.__renderer)
        self.__level_generator: LevelGenerator = LevelGenerator(self.__level_data_ref.to_dict())
        self.__level_generator.generate_sprites(self.__sprite_manager)
        self.__sprite_manager.flush_all()

        self.__sprite_manager.get_single(Vortex.Vortex).state = "stationary"

        self.__game_surf = pygame.Surface(Constants.cscale(1000, 600))

    def run(self, screen: pygame.Surface, menu: Menu):
        self.__sprite_manager.render_level(menu, self.__game_surf)
        screen.blit(self.__game_surf, Constants.cscale(15, 15))

    def __draw_toolbar(self):
        pass

    def do_persist(self) -> bool: return False
