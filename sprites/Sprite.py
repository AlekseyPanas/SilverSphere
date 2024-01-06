from __future__ import annotations
import pygame
import Constants
import copy
import Menu
from abc import abstractmethod
from game.Renderers import RenderData
from managers import GameManager
from game import SpritesManager
import enum


class ZHeights:
    MARBLE_HEIGHT = 0.0
    WATER_SHADOW_HEIGHT = 0.01
    UNDERWATER_OBJECT_HEIGHT = 1.0
    WATER_HEIGHT = 1.01
    GROUND_HEIGHT = 1.5
    GROUND_SHADOW_HEIGHT = 1.501
    X_HEIGHT = 1.7
    ON_GROUND_OBJECT_HEIGHT = 2.5
    EXPLOSION_HEIGHT = 3


class Sprite:
    def __init__(self, lifetime: int | None, z_order: float):
        self.lifetime: int | None = lifetime
        self.kill = False

        # Draw order and height reference
        self.z_order: float = z_order

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    @staticmethod
    def get_center_from_coords(coords):
        """Gets tile center from level grid coordinates (position not scaled to resolution)"""
        return (coords[0] * 50) + 25, (coords[1] * 50) + 25

    @abstractmethod
    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        """Update game data of this sprite object and add/remove any sprites via sprite_manager"""

    @abstractmethod
    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        """Return object's render data"""

    @abstractmethod
    def get_shadow(self) -> pygame.Surface | None:
        """Return None if this object casts no shadow. Otherwise, return a Surface
        which represents the shadow this object would cast if it was directly on the
        ground"""


    #
    # BORDER_IMAGE: pygame.Surface = PreAsset("assets/images/border.png", (1030, 700))  # Level Border Image

    # WATER_SHADOW_IMAGE: pygame.Surface = PreAsset("assets/images/shadow 2.png", (100, 100))  # tile shadow

# # Takes a surface along with 2 scale factors (ie. .3, 1.5, 2, etc)
# # Uses the scale factors combined with the time to make the object grow on screen over time
# # Includes additional option allowing the user to fade the object
# class InflateSurface(Object):
#     def __init__(self, lifetime, z_order, tags, surface, start_scale, stop_scale, scale_time, pos, fade=False,
#                  initial_opacity=255, delay_inflation=0):
#         super().__init__(lifetime, z_order, tags)
#
#         self.surface_rect = surface.get_rect()
#
#         self.pos = pos
#
#         self.start_scale = (self.surface_rect.w * start_scale, self.surface_rect.h * start_scale)
#         self.stop_scale = (self.surface_rect.w * stop_scale, self.surface_rect.h * stop_scale)
#         self.scale_time = scale_time
#         self.current_scale = list(copy.copy(self.start_scale))
#         self.scale_increment = ((self.stop_scale[0] - self.start_scale[0]) / self.scale_time,
#                                 (self.stop_scale[1] - self.start_scale[1]) / self.scale_time)
#
#         self.surface = pygame.Surface(self.surface_rect.size, pygame.SRCALPHA, 32)
#         self.surface.blit(surface, (0, 0))
#
#         self.opacity = initial_opacity
#         self.fade_increment = (self.opacity + 1) / self.scale_time
#         self.fade = fade
#
#         # Delays inflation for a given amount of time
#         self.delay_inflation = delay_inflation
#
#     def run_sprite(self, screen, update_lock):
#         if not update_lock:
#             if self.delay_inflation == 0:
#                 self.update()
#             else:
#                 self.delay_inflation -= 1
#         self.draw(screen)
#
#     def update(self):
#         if self.current_scale[0] < self.stop_scale[0]:
#             self.current_scale[0] += self.scale_increment[0]
#             self.current_scale[1] += self.scale_increment[1]
#         if self.fade:
#             self.opacity -= self.fade_increment
#
#     def draw(self, screen):
#         new_surf = pygame.transform.scale(self.surface, [int(x) for x in self.current_scale]).convert_alpha()
#         rect = new_surf.get_rect()
#         rect.center = self.pos
#
#         if self.fade:
#             new_surf.fill((255, 255, 255, self.opacity if self.opacity >= 0 else 0), None, pygame.BLEND_RGBA_MULT)
#
#         screen.blit(new_surf, rect)
