from __future__ import annotations
import pygame
from Constants import path2asset, cscale
import Menu
from game.Renderers import RenderData
from managers.Managers import PreAsset, ASSET_LOADER, register_assets
from sprites.Sprite import Sprite, ZHeights
from sprites.Vortex import Vortex
from sprites import Player
from managers import GameManager
from game import SpritesManager


@register_assets(ASSET_LOADER)
class Box(Sprite):
    BOX_IMAGE: pygame.Surface = PreAsset(path2asset("images/Wooden crate.png"), (50, 50))
    ICE_IMAGE: pygame.Surface = PreAsset(path2asset("images/icecube.png"), (50, 50))
    SHADOW_BOX: pygame.Surface = PreAsset(path2asset("images/box_shadow.png"), (100, 100))

    def __init__(self, lifetime, z_order, coords):
        super().__init__(lifetime, z_order)

        # Position and state
        self.coords = coords
        self.pos = list(Sprite.get_center_from_coords(coords))
        self.state = "stationary"

        # Used to track movement
        self.move_count = 0

        # dictionary to match strings with index
        self.direction_dict = {'r': 0, 'l': 1, 'u': 2, 'd': 3}

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        self.move(game_manager, sprite_manager)

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.BOX_IMAGE, self.BOX_IMAGE.get_rect(center=tuple(cscale(*self.pos))))

    def get_shadow(self) -> tuple[pygame.Surface, tuple[float, float]] | None:
        return self.SHADOW_BOX.copy(), (self.pos[0] - 25, self.pos[1] - 25)

    def detect(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # Right,Left,Up,Down
        allowed_movement = [True for x in range(4)]
        # Detects if the end of the map is in any direction of the player
        if self.coords[0] == 19:
            allowed_movement[0] = False
        if self.coords[0] == 0:
            allowed_movement[1] = False
        if self.coords[1] == 11:
            allowed_movement[3] = False
        if self.coords[1] == 0:
            allowed_movement[2] = False

        # Detects metal boxes
        if allowed_movement[0] and game_manager.get_layout()[int(self.coords[1])][int(self.coords[0]) + 1] == 'B':
            allowed_movement[0] = False
        if allowed_movement[1] and game_manager.get_layout()[int(self.coords[1])][int(self.coords[0]) - 1] == 'B':
            allowed_movement[1] = False
        if allowed_movement[2] and game_manager.get_layout()[int(self.coords[1]) - 1][int(self.coords[0])] == 'B':
            allowed_movement[2] = False
        if allowed_movement[3] and game_manager.get_layout()[int(self.coords[1]) + 1][int(self.coords[0])] == 'B':
            allowed_movement[3] = False

        # Detects other boxes
        for box in sprite_manager.get_groups([Box, IceCube]):
            box: Box
            if not box.state == 'drown':
                if allowed_movement[0] and box.coords == [self.coords[0] + 1, self.coords[1]]:
                    allowed_movement[0] = False
                if allowed_movement[1] and box.coords == [self.coords[0] - 1, self.coords[1]]:
                    allowed_movement[1] = False
                if allowed_movement[2] and box.coords == [self.coords[0], self.coords[1] - 1]:
                    allowed_movement[2] = False
                if allowed_movement[3] and box.coords == [self.coords[0], self.coords[1] + 1]:
                    allowed_movement[3] = False

        # Detects Vortex in all 4 directions
        vortex: Vortex = sprite_manager.get_single(Vortex)
        if vortex.state == 'stationary':
            if allowed_movement[0] and vortex.coords == [self.coords[0] + 1, self.coords[1]]:
                allowed_movement[0] = False
            if allowed_movement[1] and vortex.coords == [self.coords[0] - 1, self.coords[1]]:
                allowed_movement[1] = False
            if allowed_movement[2] and vortex.coords == [self.coords[0], self.coords[1] - 1]:
                allowed_movement[2] = False
            if allowed_movement[3] and vortex.coords == [self.coords[0], self.coords[1] + 1]:
                allowed_movement[3] = False

        # Returns an array which says whether or not movement in a certain direction is allowed
        # [Right,Left,Up,Down]
        return allowed_movement

    def set_drown(self):
        self.state = 'drown'
        self.z_order = ZHeights.UNDERWATER_OBJECT_HEIGHT

    def post_detect(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # detects if on water, and if so, makes the box's state 'drown' and sets the map tile to 'S' so the player can
        # move on it like a normal tile and not drown
        if game_manager.get_layout()[int(self.coords[1])][int(self.coords[0])] == 'W':
            self.set_drown()
            game_manager.set_layout_solid_at(int(self.coords[1]), int(self.coords[0]))

    def move(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # If any directional state is the current state, then run the code
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            speed = sprite_manager.get_single(Player.Player).speed
            diff = 50 - self.move_count
            # Moves box continuously in direction corresponding to the state
            if self.state == "r":
                if diff < speed:
                    self.pos[0] = round(self.pos[0] + diff)
                else:
                    self.pos[0] += speed
            elif self.state == "l":
                if diff < speed:
                    self.pos[0] = round(self.pos[0] - diff)
                else:
                    self.pos[0] -= speed
            elif self.state == "u":
                if diff < speed:
                    self.pos[1] = round(self.pos[1] - diff)
                else:
                    self.pos[1] -= speed
            elif self.state == "d":
                if diff < speed:
                    self.pos[1] = round(self.pos[1] + diff)
                else:
                    self.pos[1] += speed
            # Increment count
            self.move_count += speed
            # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
            if self.move_count >= 50:
                self.state = "stationary"
                self.move_count = 0
                # Updates Coords and runs post-detect
                self.coords = [(self.pos[0] - 25) / 50, (self.pos[1] - 25) / 50]
                self.post_detect(game_manager, sprite_manager)


class IceCube(Box):
    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.ICE_IMAGE, self.ICE_IMAGE.get_rect(center=cscale(*self.pos)))

    def move(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # If any directional state is the current state, then run the code
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            speed = sprite_manager.get_single(Player.Player).speed
            diff = 50 - self.move_count
            # Moves box continuously in direction corresponding to the state
            if self.state == "r":
                if diff < speed:
                    self.pos[0] = round(self.pos[0] + diff)
                else:
                    self.pos[0] += speed
            elif self.state == "l":
                if diff < speed:
                    self.pos[0] = round(self.pos[0] - diff)
                else:
                    self.pos[0] -= speed
            elif self.state == "u":
                if diff < speed:
                    self.pos[1] = round(self.pos[1] - diff)
                else:
                    self.pos[1] -= speed
            elif self.state == "d":
                if diff < speed:
                    self.pos[1] = round(self.pos[1] + diff)
                else:
                    self.pos[1] += speed
            # Increment count
            self.move_count += speed
            # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
            if self.move_count >= 50:
                self.coords = [(self.pos[0] - 25) / 50, (self.pos[1] - 25) / 50]
                if not self.detect(game_manager, sprite_manager)[self.direction_dict[self.state]]:
                    self.state = "stationary"
                    self.move_count = 0
                    # runs post-detect
                    self.post_detect(game_manager, sprite_manager)
                else:
                    self.move_count = 0
                    self.post_detect(game_manager, sprite_manager)
