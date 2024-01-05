from __future__ import annotations
import pygame
import Constants
import Menu
from game import SpritesManager
from game.Renderers import RenderData
from managers import GameManager
from sprites.Sprite import Sprite
from abc import abstractmethod


class ShadowManager(Sprite):
    @abstractmethod
    def register_shadow(self, sprite: Sprite):
        """This sprite has a valid shadow acquirable via get_shadow(). Use this data
        to modify the shadow surface"""


class GroundShadowManager(ShadowManager):
    def __init__(self, lifetime: int | None, z_order: float):
        super().__init__(lifetime, z_order)

    def register_shadow(self, sprite: Sprite):
        pass

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData:
        pass

    def get_shadow(self) -> pygame.Surface | None:
        pass


class WaterShadowManager(ShadowManager):
    def __init__(self, lifetime: int | None, z_order: float, water_shadow_static: pygame.mask.Mask):
        super().__init__(lifetime, z_order)

    def register_shadow(self, sprite: Sprite):
        pass

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData:
        pass

    def get_shadow(self) -> pygame.Surface | None:
        pass
