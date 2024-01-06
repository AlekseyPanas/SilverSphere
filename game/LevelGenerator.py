import pygame
import Constants
from sprites.Sprite import Sprite
from sprites.Player import Player
from sprites.X import X_Box_Tile, X_Ice_Tile
from sprites.StaticImage import StaticImage
from sprites.Vortex import Vortex
from sprites.Box import Box, IceCube
from sprites.Enemy import Enemy
import time
import Button
import copy
from sprites.Sprite import ZHeights
from game.SpritesManager import GroupSpritesManager
from managers.Managers import PreAsset, register_assets, ASSET_LOADER
from enum import IntEnum


@register_assets(ASSET_LOADER)
class LevelGenerator:
    """Given level JSON, compute level assets and generate all sprites"""
    # Tile Images
    FLOOR_TILE_IMAGE: pygame.Surface = PreAsset("assets/images/floor.png", (50, 50), False)
    IRON_TILE_IMAGE: pygame.Surface = PreAsset("assets/images/iron.png", (50, 50), False)
    WATER_IMAGE: pygame.Surface = PreAsset("assets/images/water.png", (1000, 600))  # Translucent blue water overlay
    MARBLE_IMAGE: pygame.Surface = PreAsset("assets/images/marble background.png", (1000, 600))  # Underwater floor background

    def __init__(self, level_json: dict):
        self.__level_json = level_json

    def generate_sprites(self, sprite_manager: GroupSpritesManager):
        """Add all sprites to the passed sprite manager"""
        tile_grid, metal_grid = self.__generate_grid()

        sprite_manager.add_sprite(Player(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, self.__level_json["player_start"]))  # Add player
        sprite_manager.add_sprite(StaticImage(None, ZHeights.GROUND_HEIGHT, tile_grid))  # Add ground tiles
        sprite_manager.add_sprite(StaticImage(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, metal_grid))  # Add metal boxes
        sprite_manager.add_sprite(StaticImage(None, ZHeights.MARBLE_HEIGHT, self.MARBLE_IMAGE))  # Add marble
        sprite_manager.add_sprite(StaticImage(None, ZHeights.WATER_HEIGHT, self.WATER_IMAGE))  # Add water overlay

        # Adds X tiles
        for pos in self.__level_json["ice_x_poses"]:
            sprite_manager.add_sprite(X_Ice_Tile(None, ZHeights.X_HEIGHT, pos))
        for pos in self.__level_json["box_x_poses"]:
            sprite_manager.add_sprite(X_Box_Tile(None, ZHeights.X_HEIGHT, pos))

        # Adds vortex to sprites list
        sprite_manager.add_sprite(Vortex(None, ZHeights.X_HEIGHT, self.__level_json["vortex_pos"]))

        # Adds boxes
        for idx, box_pos in enumerate(self.__level_json["box_poses"]):
            if self.__level_json["box_types"][idx] == "ice":
                sprite_manager.add_sprite(IceCube(None, 10, box_pos))
            else:
                sprite_manager.add_sprite(Box(None, 10, box_pos))

        # Adds enemies
        for enemy in self.__level_json["enemies"]:
            sprite_manager.add_sprite(
                Enemy(None, ZHeights.ON_GROUND_OBJECT_HEIGHT, enemy["start_pos"], enemy["path_dir"], enemy["path_dist"]))

    def __generate_grid(self) -> tuple[pygame.Surface, pygame.Surface]:
        """Generate tile grid and metal grid"""
        ground_layout = self.__level_json["layout"]

        # Adds image of ground layout to sprites
        tile_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)
        metal_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)
        water_shadow_surf = pygame.mask.Mask((1000, 600))

        # Draws the ground_layout
        grid_position = [0, 0]
        for row in ground_layout:
            for tile in row:
                if tile == "T":
                    tile_surf.blit(self.FLOOR_TILE_IMAGE, grid_position)
                elif tile == "B":
                    metal_surf.blit(self.IRON_TILE_IMAGE, grid_position)
                grid_position[0] += 50
            grid_position[1] += 50
            grid_position[0] = 0

        tile_surf = pygame.transform.smoothscale(tile_surf, Constants.cscale(1000, 600)).convert_alpha()
        metal_surf = pygame.transform.smoothscale(metal_surf, Constants.cscale(1000, 600)).convert_alpha()

        return tile_surf, metal_surf
