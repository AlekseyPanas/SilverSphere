from __future__ import annotations
import pygame
import Constants
from Constants import path2asset, spritesheet2frames
import Menu
from game.Renderers import RenderData
from managers.Managers import PreAsset, ASSET_LOADER, register_assets
from sprites.Sprite import Sprite
from managers import GameManager
from game import SpritesManager


@register_assets(ASSET_LOADER)
class Vortex(Sprite):
    # Vortex animations
    VORTEX_TILE_IMAGE: pygame.Surface = PreAsset(path2asset("images/vortex anim.png"), (770, 70))
    VORTEX_OPEN_IMAGE: pygame.Surface = PreAsset(path2asset("images/vortex open.png"), (630, 70))
    VORTEX_CLOSE_IMAGE: pygame.Surface = PreAsset(path2asset("images/vortex close.png"), (630, 70))

    def __init__(self, lifetime: int | None, z_order: float, coords: tuple[int, int]):
        super().__init__(lifetime, z_order)

        self.coords = coords
        self.pos = Sprite.get_center_from_coords(self.coords)
        self.state = 'blank'

        # Vortex animation images
        self.open = spritesheet2frames(self.VORTEX_OPEN_IMAGE, (9, 1))
        self.close = spritesheet2frames(self.VORTEX_CLOSE_IMAGE, (9, 1))
        self.stationary = spritesheet2frames(self.VORTEX_TILE_IMAGE, (11, 1))

        self.current_image = None
        self.current_index = 0

        # run once variable to set image
        self.set_image = False

        # animation variables   frames, and animation speed
        self.time = 0
        self.frames = 1
        self.animation_speed = None

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        if self.state == 'open' or self.state == 'close':

            # sets image, frames, and animation speed, resets time to start animation from the beginning
            if not self.set_image and self.state == 'close':
                self.current_image = self.close
                self.set_image = True
                self.frames = 9
                self.animation_speed = 0.35
                self.time = 0
            elif not self.set_image and self.state == 'open':
                self.current_image = self.open
                self.set_image = True
                self.frames = 9
                self.animation_speed = 0.35
                self.time = 0

        elif self.state == 'stationary':
            if not self.set_image:
                self.current_image = self.stationary
                self.set_image = True
                self.frames = 11
                self.animation_speed = 0.28
                self.time = 0

            # FIX THIS: Checks for boxes on open vortex and sets them to explode
            # for box in sprite_manager.get_group(Box):
            #     if box.coords == self.coords:
            #         box.kill = True
            #         sprite_manager.add_sprite(Animation(-1, 12, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
            #                                              Constants.cscale(*box.pos), 74))

        else:
            self.current_image = None

        if self.state != "blank":
            self.animate()

    def animate(self):
        self.current_index = int(self.time % self.frames)

        self.time += self.animation_speed
        # Checks if animation ended
        if self.state == 'open' or self.state == 'close':
            if self.time > 1 and int(self.time % self.frames) == 0:
                if self.state == 'open':
                    self.state = 'stationary'
                elif self.state == 'close':
                    self.state = 'blank'
                self.set_image = False

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        if self.state == "blank" or self.current_image is None:
            return None
        return RenderData(self.z_order, self.current_image[self.current_index], Constants.cscale(*self.pos), False)

    def get_shadow(self) -> pygame.Surface | None: return None
