from __future__ import annotations
import pygame
from Constants import cscale, path2asset
import Menu
from game.Renderers import RenderData
from managers.Managers import PreAsset, AnimationPreAsset, ASSET_LOADER, register_assets
from sprites.Sprite import Sprite, ZHeights
from managers import GameManager
from game import SpritesManager


class AnimationEffect(Sprite):
    def __init__(self, lifetime: int | None, z_order: float, frames: list[pygame.Surface],
                 ticks_per_frame: float, world_center: tuple[float, float]):
        super().__init__(lifetime, z_order)
        self.__frames = frames
        self.__ticks_per_frame = ticks_per_frame
        self.__counter = 0
        self.__idx = 0
        self.__world_center = world_center

    def update(self, menu: Menu, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        """Update animation variables and kill upon animation finish"""
        self.__counter += 1
        if self.__counter > self.__ticks_per_frame * len(self.__frames):
            self.kill = True
        self.__idx = int(min(self.__counter // self.__ticks_per_frame, len(self.__frames) - 1))

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.__frames[self.__idx], cscale(*self.__world_center), False)

    def get_shadow(self) -> pygame.Surface | None: return None


@register_assets(ASSET_LOADER)
class ExplosionAnimation(AnimationEffect):
    EXPLOSION_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/explosion.png"), (100, 100), True, (9, 9), 2, False)  # Explosion animation

    def __init__(self, world_center: tuple[float, float]):
        super().__init__(None, ZHeights.EXPLOSION_HEIGHT, self.EXPLOSION_IMAGE, 1, world_center)
