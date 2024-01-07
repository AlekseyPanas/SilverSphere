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
    WATER_SPLASH_HEIGHT = 1.02
    GROUND_HEIGHT = 1.5
    X_HEIGHT = 1.5001
    GROUND_SHADOW_HEIGHT = 1.501
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
    def get_shadow(self) -> tuple[pygame.Surface, tuple[float, float]] | None:
        """Return None if this object casts no shadow. Otherwise, return a Surface
        which represents the shadow this object would cast if it was directly on the
        ground. The shadow surface returned should be resolution-scaled. Also return
        topleft corner in world coordinates"""
