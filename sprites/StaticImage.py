from __future__ import annotations
import pygame
import Constants
import Menu
from game.Renderers import RenderData
from sprites.Sprite import Sprite
from sprites.ShadowManager import ShadowManager
from managers import GameManager
from game import SpritesManager


class StaticImage(Sprite):
    def __init__(self, lifetime: int | None, z_order: float, image: pygame.Surface, topleft=(0, 0)):
        super().__init__(lifetime, z_order)
        self.__image = image
        self.__topleft = topleft

    def update(self, menu: Menu, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager): pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.__image, self.__topleft, True)

    def get_shadow(self) -> pygame.Surface | None: return None
