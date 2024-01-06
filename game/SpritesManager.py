from __future__ import annotations
from sprites.Sprite import Sprite
from sprites.ShadowManager import ShadowManager
from typing import Iterable


class SpriteGroup:
    def __init__(self, t: type):
        self.t: type = t
        self.__sprites: list[Sprite] = []
        self.__sprite_add_queue: list[Sprite] = []
        self.__sprite_delete_queue: list[Sprite] = []

    def add_sprite(self, sprite: Sprite):
        """Queue sprite for addition"""
        self.__sprite_add_queue.append(sprite)

    def delete_sprite(self, sprite: Sprite):
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
    def __init__(self, level_json: dict):
        self.__level_json = level_json
        self.__sprite_groups: dict[type, SpriteGroup] = dict()
        self.__shadow_managers: SpriteGroup = SpriteGroup(ShadowManager)

    def __exists_group(self, t: type):
        return self.__sprite_groups.get(t, None) is not None

    def add_sprite(self, sprite: Sprite):
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
            self.__sprite_groups[type(sprite)] = new_group
            new_group.add_sprite(sprite)

    def remove_sprite(self, sprite: Sprite):
        """Delete sprite. Does not throw errors if sprite didnt exist"""
        # Remove from shadow managers if descendent
        if isinstance(sprite, ShadowManager):
            self.__shadow_managers.delete_sprite(sprite)
            return

        # Remove from appropriate group
        if self.__exists_group(type(sprite)):
            self.__sprite_groups[type(sprite)].delete_sprite(sprite)

    def get_single(self, t: type) -> Sprite:
        """Get single sprite from the sprite group of type t. Intended for convenience for groups with only
        one item"""
        return self.get_group(t)[0]

    def get_group(self, t: type) -> list[Sprite]:
        """Get list of sprites of type t, or empty list if none, excluding shadow managers"""
        if self.__exists_group(t):
            return self.__sprite_groups[t].get_sprites()
        return []

    def get_groups(self, ts: list[type]) -> Iterable[Sprite]:
        """Get a list of sprites of any type in ts, excluding shadow managers"""
        for t in ts:
            for sprite in self.get_group(t):
                yield sprite

    def get_all_sprites(self) -> Iterable[Sprite]:
        """Get all sprites excluding shadow managers"""
        for g in self.__sprite_groups.values():
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
