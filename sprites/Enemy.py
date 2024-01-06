from __future__ import annotations
import pygame
import copy
import Menu
from game.Renderers import RenderData
from sprites.Sprite import Sprite, ZHeights
from sprites.Player import Player
from sprites.Box import IceCube, Box
from managers.Managers import PreAsset, AnimationPreAsset, ASSET_LOADER, register_assets
from Constants import spritesheet2frames, path2asset, scale_surfaces
import Constants
from managers import GameManager
from game import SpritesManager


@register_assets(ASSET_LOADER)
class Enemy(Sprite):
    ENEMY_IMAGE: pygame.Surface = PreAsset(path2asset("images/Golden Ball.png"), (51, 51))
    ENEMY_UP_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Gold Up.png"), (51, 51), True, (4, 1))
    ENEMY_DOWN_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Gold Down.png"), (51, 51), True, (4, 1))
    ENEMY_RIGHT_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Gold Right.png"), (51, 51), True, (4, 1))
    ENEMY_LEFT_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Gold Left.png"), (51, 51), True, (4, 1))

    def __init__(self, lifetime: int | None, z_order: float,
                 coords: tuple[int, int], path_dir: list[int], path_dist: list[int]):
        super().__init__(lifetime, z_order)
        # Paths: [direction array ie "u", "d", "r", "l"] [distance array]
        self.image = self.ENEMY_IMAGE
        self.img_l = self.ENEMY_LEFT_IMAGE
        self.img_r = self.ENEMY_RIGHT_IMAGE
        self.img_u = self.ENEMY_UP_IMAGE
        self.img_d = self.ENEMY_DOWN_IMAGE
        self.__current_index = 0

        self.path_dir = path_dir
        self.path_dist = path_dist
        self.path_index = 0
        self.path_dist_counter = 0

        self.dir_dict = {"u": self.img_u, "d": self.img_d, "r": self.img_r, "l": self.img_l}
        self.dir = self.path_dir[0]

        self.current_image = self.dir_dict[self.dir]

        self.time = 0

        self.coords = coords
        self.pos = list(Sprite.get_center_from_coords(coords))
        self.move_count = 0
        self.save_pos = copy.copy(self.pos)

        self.speed = 6

    def set_drown(self):
        self.dir = 'drown'
        self.z_order = ZHeights.UNDERWATER_OBJECT_HEIGHT

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        self.move(game_manager)
        if not self.dir == "drown":
            self.collisions(sprite_manager)
            self.animate()

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        return RenderData(self.z_order, self.current_image[self.__current_index], tuple(Constants.cscale(*self.pos)), False)

    def get_shadow(self) -> pygame.Surface | None: return None

    def animate(self):
        self.__current_index = int((self.time % 24) // 6)
        self.time += 0.95

    def collisions(self, sprite_manager: SpritesManager.GroupSpritesManager):
        explode_list = []
        explode = False

        for sprite in sprite_manager.get_groups([Player, Box, IceCube]):
            dist = Constants.distance(self.pos, sprite.pos)
            if not sprite.state == "drown":
                if dist < 50:
                    explode = True
                if dist < 75:
                    explode_list.append(sprite)

        if explode:
            for sprite in explode_list:
                if isinstance(sprite, Player):
                    sprite.set_drown()
                    # Globe.MENU.game.reset = True
                else:
                    sprite.kill = True
                self.kill = True
                # Globe.MENU.game.add_sprite(Animation(-1, 15, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
                #                                      Constants.cscale(*sprite.pos), 74))
        # if self.kill:
        #     Globe.MENU.game.add_sprite(Animation(-1, 15, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
        #                                          Constants.cscale(*self.pos), 74))

    def move(self, game_manager: GameManager):
        if not self.dir == "drown":
            diff = 50 - self.move_count
            if self.dir == "u":
                if diff < self.speed:
                    self.pos[1] = round(self.pos[1] - diff)
                else:
                    self.pos[1] -= self.speed

            elif self.dir == "d":
                if diff < self.speed:
                    self.pos[1] = round(self.pos[1] + diff)
                else:
                    self.pos[1] += self.speed

            elif self.dir == "r":
                if diff < self.speed:
                    self.pos[0] = round(self.pos[0] + diff)
                else:
                    self.pos[0] += self.speed

            elif self.dir == "l":
                if diff < self.speed:
                    self.pos[0] = round(self.pos[0] - diff)
                else:
                    self.pos[0] -= self.speed

            self.move_count += self.speed

            if self.move_count >= 50:
                self.move_count = 0
                self.path_dist_counter += 1

                if self.path_dist_counter == self.path_dist[self.path_index]:
                    self.path_dist_counter = 0

                    self.path_index += 1
                    if self.path_index >= len(self.path_dir):
                        self.path_index = 0

                    self.dir = self.path_dir[self.path_index]
                    self.current_image = self.dir_dict[self.dir]

                self.coords = [(self.pos[0] - 25) / 50, (self.pos[1] - 25) / 50]

                if game_manager.get_layout()[int(self.coords[1])][int(self.coords[0])] == "W":
                    self.set_drown()
