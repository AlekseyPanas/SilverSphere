from __future__ import annotations
import pygame
from Constants import cscale, path2asset
import Menu
from game.Renderers import RenderData
from managers.Managers import PreAsset, AnimationPreAsset, ASSET_LOADER, register_assets
from sprites.Sprite import Sprite, ZHeights
from managers import GameManager
from game import SpritesManager
from enum import IntEnum
import copy
import random


class InflateSurface:
    """
    Takes a surface along with 2 scale factors (ie. .3, 1.5, 2, etc)
    Uses the scale factors combined with the time to make the object grow on screen over time
    Includes additional option allowing the user to fade the object
    """
    def __init__(self, z_order: float, surface: pygame.Surface, start_scale: float, stop_scale: float,
                 scale_time: float, center: tuple[int, int], fade=False, initial_opacity=255, delay_inflation=0):
        self.surface_rect = surface.get_rect()

        self.pos = center
        self.z_order = z_order

        self.start_scale = (self.surface_rect.w * start_scale, self.surface_rect.h * start_scale)
        self.stop_scale = (self.surface_rect.w * stop_scale, self.surface_rect.h * stop_scale)
        self.scale_time = scale_time
        self.current_scale = list(copy.copy(self.start_scale))
        self.scale_increment = ((self.stop_scale[0] - self.start_scale[0]) / self.scale_time,
                                (self.stop_scale[1] - self.start_scale[1]) / self.scale_time)

        self.surface = pygame.Surface(self.surface_rect.size, pygame.SRCALPHA, 32)
        self.surface.blit(surface, (0, 0))

        self.opacity = initial_opacity
        self.fade_increment = (self.opacity + 1) / self.scale_time
        self.fade = fade

        # Delays inflation for a given amount of time
        self.delay_inflation = delay_inflation

    def render(self) -> RenderData | None:
        new_surf = pygame.transform.smoothscale(self.surface, [int(x) for x in self.current_scale]).convert_alpha()
        rect = new_surf.get_rect()
        rect.center = self.pos

        if self.fade:
            new_surf.fill((255, 255, 255, self.opacity if self.opacity >= 0 else 0), None, pygame.BLEND_RGBA_MULT)

        return RenderData(self.z_order, new_surf, rect)

    def update(self):
        if self.delay_inflation == 0:
            if self.current_scale[0] < self.stop_scale[0]:
                self.current_scale[0] += self.scale_increment[0]
                self.current_scale[1] += self.scale_increment[1]
            if self.fade:
                self.opacity -= self.fade_increment
        else:
            self.delay_inflation -= 1


class InflateSurfaceSprite(Sprite):
    """Thin wrapper to make an inflate surface a sprite object"""
    def __init__(self, lifetime: int | None, z_order: float, surface: pygame.Surface, start_scale: float, stop_scale: float,
                 scale_time: float, center: tuple[int, int], fade=False, initial_opacity=255, delay_inflation=0):
        """
        :param lifetime:
        :param z_order:
        :param surface: Surface to inflate
        :param start_scale: Multiplicative factor of initial surface size to start with
        :param stop_scale: Scale factor to end with
        :param scale_time: Ticks to scale
        :param center: resolution-scaled center position
        :param fade: Should the surface fade out as it scales
        :param initial_opacity: if fading, what opacity to start with (ends with full transparency)
        :param delay_inflation: Ticks to delay the inflation
        """
        super().__init__(lifetime, z_order)
        self.__inflate_surf = InflateSurface(z_order, surface, start_scale, stop_scale, scale_time, center, fade, initial_opacity, delay_inflation)

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return self.__inflate_surf.render()

    def get_shadow(self) -> pygame.Surface | None: return None

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        self.__inflate_surf.update()
        if self.__inflate_surf.opacity < 0:
            self.kill = True


class SplashTypes(IntEnum):
    SPHERE_SMALL = 0
    SPHERE_BIG = 1
    BOX_SMALL = 2
    BOX_BIG = 3


@register_assets(ASSET_LOADER)
class SplashSphereSmall(InflateSurfaceSprite):
    __rad = 120
    __thickness = 20
    __surf_dim = (__rad + __thickness) * 2
    __surf = pygame.Surface((__surf_dim, __surf_dim), pygame.SRCALPHA, 32)
    pygame.draw.circle(__surf, (255, 255, 255), (__surf_dim // 2, __surf_dim // 2), __rad, __thickness)
    SPLASH: pygame.Surface = PreAsset(__surf, __surf.get_size())

    def __init__(self, center: tuple[int, int]):
        """
        :param center: resolution-scaled center
        """
        super().__init__(None, ZHeights.WATER_SPLASH_HEIGHT, self.SPLASH, 0, 1, 40, center, fade=True, initial_opacity=150)


@register_assets(ASSET_LOADER)
class SplashSphereBig(InflateSurfaceSprite):
    __rad = 160
    __thickness = 15
    __surf_dim = (__rad + __thickness) * 2
    __surf = pygame.Surface((__surf_dim, __surf_dim), pygame.SRCALPHA, 32)
    pygame.draw.circle(__surf, (255, 255, 255), (__surf_dim // 2, __surf_dim // 2), __rad, __thickness)
    SPLASH: pygame.Surface = PreAsset(__surf, __surf.get_size())

    def __init__(self, center: tuple[int, int]):
        """
        :param center: resolution-scaled center
        """
        super().__init__(None, ZHeights.WATER_SPLASH_HEIGHT, self.SPLASH, 0, 1, 30, center, fade=True, initial_opacity=150)


@register_assets(ASSET_LOADER)
class SplashBoxSmall(InflateSurfaceSprite):
    __rad = 90
    __thickness = 16
    __surf_dim = (__rad + __thickness) * 2
    __surf = pygame.Surface((__surf_dim, __surf_dim), pygame.SRCALPHA, 32)
    pygame.draw.rect(__surf, (255, 255, 255), (__thickness, __thickness, __rad * 2, __rad * 2), __thickness, 70)
    SPLASH: pygame.Surface = PreAsset(__surf, __surf.get_size())

    def __init__(self, center: tuple[int, int]):
        """
        :param center: resolution-scaled center
        """
        super().__init__(None, ZHeights.WATER_SPLASH_HEIGHT, self.SPLASH, 0, 1, 40, center, fade=True, initial_opacity=150)


@register_assets(ASSET_LOADER)
class SplashBoxBig(InflateSurfaceSprite):
    __rad = 130
    __thickness = 13
    __surf_dim = (__rad + __thickness) * 2
    __surf = pygame.Surface((__surf_dim, __surf_dim), pygame.SRCALPHA, 32)
    pygame.draw.rect(__surf, (255, 255, 255), (__thickness, __thickness, __rad * 2, __rad * 2), __thickness, 70)
    SPLASH: pygame.Surface = PreAsset(__surf, __surf.get_size())

    def __init__(self, center: tuple[int, int]):
        """
        :param center: resolution-scaled center
        """
        super().__init__(None, ZHeights.WATER_SPLASH_HEIGHT,
                         pygame.transform.rotate(self.SPLASH, random.randint(-20, 20)),
                         0, 1, 30, center, fade=True, initial_opacity=150)


def get_splash(center: tuple[int, int], splash_type: SplashTypes):
    match splash_type:
        case SplashTypes.SPHERE_SMALL:
            return SplashSphereSmall(center)
        case SplashTypes.SPHERE_BIG:
            return SplashSphereBig(center)
        case SplashTypes.BOX_SMALL:
            return SplashBoxSmall(center)
        case SplashTypes.BOX_BIG:
            return SplashBoxBig(center)
        case _:
            pass
