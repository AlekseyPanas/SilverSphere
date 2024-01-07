from __future__ import annotations
import pygame
import Constants
import Menu
from game import SpritesManager
from game.Renderers import RenderData
from managers import GameManager
from sprites.Sprite import Sprite, ZHeights
from sprites import Box
from abc import abstractmethod


class ShadowManager(Sprite):
    @abstractmethod
    def register_shadow(self, sprite: Sprite):
        """This sprite has a valid shadow acquirable via get_shadow(). Use this data
        to modify the shadow surface"""

    def get_shadow(self) -> pygame.Surface | None: return None


class GroundShadowManager(ShadowManager):
    def __init__(self, z_order: float, scaled_inverse_surface: pygame.Surface, metal_shadow_surf: pygame.Surface):
        """
        :param z_order:
        :param scaled_inverse_surface: A surface with (255, 255, 255, 255) values for all water pixels (to clip land shadows)
        :param metal_shadow_surf:
        """
        super().__init__(None, z_order)
        self.__base_shadow = metal_shadow_surf
        self.__cur_shadow = self.__base_shadow.copy()
        self.__clipper = scaled_inverse_surface

    def register_shadow(self, sprite: Sprite):
        height_diff = sprite.z_order - ZHeights.GROUND_HEIGHT
        if height_diff >= 0:
            surf, world_topleft = sprite.get_shadow()
            self.__cur_shadow.blit(surf, Constants.cscale(*world_topleft))

        # TODO: Hacky way of updating ground clipping. Keep in mind that this needs to happen even if the box decides
        #   to have no shadow, in which case this method would not get called
        if isinstance(sprite, Box.Box) and sprite.state == "drown":
            sprite: Box.Box
            pygame.draw.rect(self.__clipper, (0, 0, 0, 0),
                             Constants.cscale(sprite.pos[0] - 25, sprite.pos[1] - 25, 50, 50))

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager): pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        surf = self.__cur_shadow
        surf: pygame.Surface
        surf.blit(self.__clipper, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.__cur_shadow = self.__base_shadow.copy()
        return RenderData(self.z_order, surf, surf.get_rect(topleft=(0, 0)))
        #return RenderData(100, self.__clipper, surf.get_rect(topleft=(0, 0)))
        #return RenderData(100, self.__base_shadow, surf.get_rect(topleft=(0, 0)))


class WaterShadowManager(ShadowManager):
    SHADOW_COLOR = (59, 86, 102)

    def __init__(self, z_order: float, water_shadow_static: pygame.mask.Mask):
        """
        :param z_order:
        :param water_shadow_static: Resolution-scaled mask of set pixels for the tile grid shadows
        """
        super().__init__(None, z_order)
        self.__shadow_mask = water_shadow_static

        self.__cur_mask = self.__shadow_mask.copy()

    def register_shadow(self, sprite: Sprite):
        height_diff = (sprite.z_order - ZHeights.MARBLE_HEIGHT - 1) / 1.5

        surf, world_topleft = sprite.get_shadow()
        surf: pygame.Surface

        scale_factor = (height_diff * 0.01) * 5
        shift_factor_x = height_diff * 20
        shift_factor_y = height_diff * 8

        surf = pygame.transform.smoothscale(surf, tuple(p * (1 + scale_factor) for p in surf.get_size()))
        self.__cur_mask.draw(pygame.mask.from_surface(surf, 5),
                             Constants.cscale(
                                 world_topleft[0] + shift_factor_x,
                                 world_topleft[1] + shift_factor_y
                             ))

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager): pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        surf = self.__cur_mask.to_surface(setcolor=self.SHADOW_COLOR, unsetcolor=(0, 0, 0))
        surf.set_colorkey((0, 0, 0))
        self.__cur_mask = self.__shadow_mask.copy()
        return RenderData(self.z_order, surf, surf.get_rect(topleft=(0, 0)))
