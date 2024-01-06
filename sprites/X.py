from __future__ import annotations
import pygame
import Constants
from Constants import path2asset
import Menu
from game.Renderers import RenderData
from managers.Managers import PreAsset, ASSET_LOADER, register_assets
from sprites.Sprite import Sprite
from managers import GameManager
from game import SpritesManager


@register_assets(ASSET_LOADER)
class X_Box_Tile(Sprite):
    ICE_X_TILE_IMAGE: pygame.Surface = PreAsset(path2asset("images/Xice.png"), (63, 63))
    BOX_X_TILE_IMAGE: pygame.Surface = PreAsset(path2asset("images/Xbox.png"), (63, 63))

    def __init__(self, lifetime: int | None, z_order: float, coords):
        super().__init__(lifetime, z_order)
        self.coords = coords
        self.pos = [(coords[0] * 50) + 25, (coords[1] * 50) + 25]

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager): pass

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.BOX_X_TILE_IMAGE, Constants.cscale(*self.pos), False)

    def get_shadow(self) -> pygame.Surface | None: return None


class X_Ice_Tile(X_Box_Tile):
    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.ICE_X_TILE_IMAGE, Constants.cscale(*self.pos), False)
