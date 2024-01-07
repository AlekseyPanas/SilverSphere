import pygame
import Constants
from Constants import path2asset, cscale
from sprites.Player import Player
from sprites.X import X_Box_Tile, X_Ice_Tile
from sprites.StaticImage import StaticImage
from sprites.Vortex import Vortex
from sprites.Box import Box, IceCube
from sprites.Enemy import Enemy
from sprites.Sprite import ZHeights
from sprites.ShadowManager import GroundShadowManager, WaterShadowManager
from game.SpritesManager import GroupSpritesManager
from managers.Managers import PreAsset, register_assets, ASSET_LOADER


@register_assets(ASSET_LOADER)
class LevelGenerator:
    """Given level JSON, compute level assets and generate all sprites"""
    # Tile Images
    FLOOR_TILE_IMAGE: pygame.Surface = PreAsset(path2asset("images/floor.png"), (50, 50), False)
    IRON_TILE_IMAGE: pygame.Surface = PreAsset(path2asset("images/iron.png"), (50, 50), False)
    WATER_IMAGE: pygame.Surface = PreAsset(path2asset("images/water.png"), (1000, 600))  # Translucent blue water overlay
    MARBLE_IMAGE: pygame.Surface = PreAsset(path2asset("images/marble background.png"), (1000, 600))  # Underwater floor background
    SHADOW_GROUND_TILE: pygame.Surface = PreAsset(path2asset("images/shadow 2.png"), (100, 100))
    SHADOW_METAL_TILE: pygame.Surface = PreAsset(path2asset("images/shadow 2.png"), (110, 110))

    def __init__(self, level_json: dict):
        self.__level_json = level_json

    def generate_sprites(self, sprite_manager: GroupSpritesManager):
        """Add all sprites to the passed sprite manager"""
        tile_grid, metal_grid, water_shadow, grid_clipper, ground_shadow = self.__generate_grid()

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

        # Add shadow managers
        sprite_manager.add_sprite(WaterShadowManager(ZHeights.WATER_SHADOW_HEIGHT, water_shadow))
        # test_white_surf = pygame.Surface(cscale(1000, 600))  # Adds a white surface for debugging
        # test_white_surf.fill((255, 255, 255))
        # sprite_manager.add_sprite(StaticImage(None, 99, test_white_surf))
        sprite_manager.add_sprite(GroundShadowManager(ZHeights.GROUND_SHADOW_HEIGHT, grid_clipper, ground_shadow))

    def __generate_grid(self) -> tuple[pygame.Surface, pygame.Surface, pygame.Mask, pygame.Surface, pygame.Surface]:
        """Generate tile grid and metal grid"""
        ground_layout = self.__level_json["layout"]

        tile_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)
        metal_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)

        water_shadow_surf = pygame.mask.Mask(cscale(1000, 600))
        metal_ground_shadow_surf = pygame.Mask(cscale(1000, 600))  # Used to prevent overlapping metal box shadows

        # Draws the ground_layout
        grid_position = [0, 0]
        for row in ground_layout:
            for tile in row:
                if tile == "T":
                    tile_surf.blit(self.FLOOR_TILE_IMAGE, grid_position)
                    water_shadow_surf.draw(pygame.mask.from_surface(self.SHADOW_GROUND_TILE), cscale(*grid_position))
                elif tile == "B":
                    metal_surf.blit(self.IRON_TILE_IMAGE, grid_position)

                    box_mask = pygame.mask.from_surface(Box.SHADOW_BOX, 5)
                    water_shadow_surf.draw(box_mask, cscale(grid_position[0] + 12, grid_position[1] + 8))
                    metal_ground_shadow_surf.draw(box_mask, cscale(*grid_position))
                grid_position[0] += 50
            grid_position[1] += 50
            grid_position[0] = 0

        s = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)
        s.blit(tile_surf, (0, 0))
        s.blit(metal_surf, (0, 0))
        grid_clipper = pygame.transform.smoothscale(
            pygame.mask.from_surface(s).to_surface(setcolor=(0, 0, 0, 0), unsetcolor=(255, 255, 255, 255)),
            cscale(1000, 600)
        ).convert_alpha()

        tile_surf = pygame.transform.smoothscale(tile_surf, cscale(1000, 600)).convert_alpha()
        metal_surf = pygame.transform.smoothscale(metal_surf, cscale(1000, 600)).convert_alpha()

        return tile_surf, metal_surf, water_shadow_surf, grid_clipper, metal_ground_shadow_surf.to_surface(setcolor=(0, 0, 0, 50), unsetcolor=(0, 0, 0, 0))

