from __future__ import annotations
import random
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
from Constants import path2asset
import Constants


@register_assets(ASSET_LOADER)
class BirthdayManager(Manager):
    """Manager for Birthday Screen"""

    BDAY_BACKGROUND: pygame.Surface = PreAsset(path2asset("images/bdaybg.png"), (1030, 700))
    BDAY_TEXT: pygame.Surface = PreAsset(path2asset("images/bdaytext.png"), (995, 142))
    BDAY_BALLOON: pygame.Surface = PreAsset(path2asset("images/balloon.png"), (83, 219))

    def __init__(self, menu: Menu):
        # Birthday screen stuff
        super().__init__(menu)
        self.balloons = [[random.randint(20, 1010), random.randint(20, 680), random.randint(3, 12)] for x in range(5)]
        self.balloon_time = 0
        self.inflation = Sprite.InflateSurface(None, 0, {}, self.BDAY_TEXT, .01, 1, 35, Constants.cscale(515, 90))

    def run(self, screen: pygame.Surface, menu: Menu):
        screen.blit(self.BDAY_BACKGROUND, (0, 0))
        self.inflation.run_sprite(screen, False)
        for ball in self.balloons:
            screen.blit(self.BDAY_BALLOON,
                        self.BDAY_BALLOON.get_rect(center=Constants.cscale(ball[0], ball[1])))
            ball[1] -= ball[2]
        self.balloon_time += 1
        if self.balloon_time % 10 == 0:
            self.balloons.append([random.randint(20, 1010), 1000, random.randint(3, 12)])

    def do_persist(self) -> bool: return False
