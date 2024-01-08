from __future__ import annotations
import Menu
from sprites import Sprite
from sprites.ShadowManager import ShadowManager
from typing import Iterable
from copy import copy
from game.Renderers import ZHeapRenderer
import pygame


class SpriteGroup:
    def __init__(self, t: type):
        self.t: type = t
        self.__sprites: list[Sprite.Sprite] = []
        self.__sprite_add_queue: list[Sprite.Sprite] = []
        self.__sprite_delete_queue: list[Sprite.Sprite] = []

    def add_sprite(self, sprite: Sprite.Sprite):
        """Queue sprite for addition"""
        self.__sprite_add_queue.append(sprite)

    def delete_sprite(self, sprite: Sprite.Sprite):
        """Queue sprite for deletion"""
        self.__sprite_delete_queue.append(sprite)

    def get_sprites(self):
        return self.__sprites

    def flush(self):
        """Add and remove sprites based on queues and clear the queues and based on sprite death"""
        self.__sprites = [s for s in self.__sprites if (s not in self.__sprite_delete_queue) and
                          (s.lifetime is None or s.lifetime > 0) and (not s.kill)]
        self.__sprites += self.__sprite_add_queue
        self.__sprite_delete_queue = []
        self.__sprite_add_queue = []


class GroupSpritesManager:
    def __init__(self, level_json: dict, renderer: ZHeapRenderer):
        self.__level_json = level_json
        self.__sprite_groups: dict[type, SpriteGroup] = dict()
        self.__shadow_managers: SpriteGroup = SpriteGroup(ShadowManager)

        self.__renderer = renderer

    def __exists_group(self, t: type):
        return self.__sprite_groups.get(t, None) is not None

    def add_sprite(self, sprite: Sprite.Sprite):
        """Add sprite to existing group or create new one"""
        # Add if descendent of shadow managers
        if isinstance(sprite, ShadowManager):
            self.__shadow_managers.add_sprite(sprite)
            return

        # Add to group by type or create new one
        if self.__exists_group(type(sprite)):
            self.__sprite_groups[type(sprite)].add_sprite(sprite)
        else:
            new_group = SpriteGroup(type(sprite))
            new_group.add_sprite(sprite)
            self.__sprite_groups[type(sprite)] = new_group

    def remove_sprite(self, sprite: Sprite.Sprite):
        """Delete sprite. Does not throw errors if sprite didnt exist"""
        # Remove from shadow managers if descendent
        if isinstance(sprite, ShadowManager):
            self.__shadow_managers.delete_sprite(sprite)
            return

        # Remove from appropriate group
        if self.__exists_group(type(sprite)):
            self.__sprite_groups[type(sprite)].delete_sprite(sprite)

    def get_single(self, t: type) -> Sprite.Sprite:
        """Get single sprite from the sprite group of type t. Intended for convenience for groups with only
        one item"""
        return self.get_group(t)[0]

    def get_group(self, t: type) -> list[Sprite.Sprite]:
        """Get list of sprites of type t, or empty list if none, excluding shadow managers"""
        if self.__exists_group(t):
            return self.__sprite_groups[t].get_sprites()
        return []

    def get_groups(self, ts: list[type]) -> Iterable[Sprite.Sprite]:
        """Get a list of sprites of any type in ts, excluding shadow managers"""
        for t in ts:
            for sprite in self.get_group(t):
                yield sprite

    def get_all_sprites(self) -> Iterable[Sprite.Sprite]:
        """Get all sprites excluding shadow managers"""
        for g in list(self.__sprite_groups.values()):
            for sprite in g.get_sprites():
                yield sprite

    def get_shadow_managers(self) -> list[ShadowManager]:
        """Return shadow managers"""
        return self.__shadow_managers.get_sprites()

    def decrement_lifetimes(self):
        """Subtract 1 from every sprite lifetime"""
        for g in list(self.__sprite_groups.values()) + [self.__shadow_managers]:
            for spr in g.get_sprites():
                if spr.lifetime is not None:
                    spr.lifetime -= 1

    def flush_all(self):
        """Removes dead sprites and flushes all queues"""
        for g in list(self.__sprite_groups.values()) + [self.__shadow_managers]:
            g.flush()

    def render_level(self, menu: Menu.Menu, game_surface: pygame.Surface):
        """Using the injected renderer, render the game frame with all sprites onto the provided
        game_surface"""
        for s in self.get_all_sprites():
            render_output = s.render(menu, self)
            if render_output is not None:
                self.__renderer.add_to_frame(render_output)  # Render sprite

            # Register shadows
            shad = s.get_shadow()
            if shad is not None:
                for shadman in self.get_shadow_managers():
                    shadman.register_shadow(s)

        # Render shadows and add them
        for shadman in self.get_shadow_managers():
            self.__renderer.add_to_frame(shadman.render(menu, self))

        # Render frame
        self.__renderer.render_frame(game_surface)
