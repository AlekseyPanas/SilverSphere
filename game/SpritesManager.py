from sprites.Sprite import Sprite
from sprites.ShadowManager import ShadowManager


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
        self.__sprite_groups: list[SpriteGroup] = []
        self.__shadow_managers: SpriteGroup = SpriteGroup(ShadowManager)

    def add_sprite(self, sprite: Sprite):
        """Add sprite to existing group or create new one"""
        # Add if descendent of shadow managers
        if isinstance(sprite, ShadowManager):
            self.__shadow_managers.add_sprite(sprite)
            return

        # Add to group by type or create new one
        for g in self.__sprite_groups:
            if g.t == type(sprite):
                g.add_sprite(sprite)
                return
        new_group = SpriteGroup(type(sprite))
        self.__sprite_groups.append(new_group)
        new_group.add_sprite(sprite)

    def remove_sprite(self, sprite: Sprite):
        """Delete sprite. Does not throw errors if sprite didnt exist"""
        # Remove from shadow managers if descendent
        if isinstance(sprite, ShadowManager):
            self.__shadow_managers.delete_sprite(sprite)
            return

        # Remove from appropriate group
        for g in self.__sprite_groups:
            if g.t == type(sprite):
                g.delete_sprite(sprite)

    def get_group(self, t: type) -> list[Sprite]:
        """Get list of sprites of type t, or empty list if none, excluding shadow managers"""
        for g in self.__sprite_groups:
            if g.t == t:
                return g.get_sprites()
        return []

    def get_groups(self, ts: list[type]) -> list[list[Sprite]]:
        """Get a list of sprites of any type in ts, excluding shadow managers"""
        groups = []
        for t in ts:
            groups.append(self.get_group(t))
        return groups

    def get_all_sprites(self) -> list[list[Sprite]]:
        """Get all sprites excluding shadow managers"""
        return [g.get_sprites() for g in self.__sprite_groups]

    def get_shadow_managers(self) -> list[ShadowManager]:
        """Return shadow managers"""
        return self.__shadow_managers.get_sprites()

    def decrement_lifetimes(self):
        """Subtract 1 from every sprite lifetime"""
        for g in self.__sprite_groups + [self.__shadow_managers]:
            for spr in g.get_sprites():
                if spr.lifetime is not None:
                    spr.lifetime -= 1

    def flush_all(self):
        """Removes dead sprites and flushes all queues"""
        for g in self.__sprite_groups + [self.__shadow_managers]:
            g.flush()
