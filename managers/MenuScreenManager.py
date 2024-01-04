from __future__ import annotations
import pygame
from managers.Managers import Manager, ASSET_LOADER, register_assets, PreAsset
import Menu
import Constants
from abc import abstractmethod
from Constants import path2asset


@register_assets(ASSET_LOADER)
class MenuScreenManager(Manager):
    """Manager for main menu screen"""
    MENU_FOREGROUND_IMAGE: pygame.Surface = PreAsset(path2asset("images/title screen.png"), (1030, 700))
    MENU_SKY_IMAGE: pygame.Surface = PreAsset(path2asset("images/cloud.png"), (1030, 700))

    # Static variables to preserve across inheriting classes
    # Background moving sky image position tracking
    skys = [Constants.posscale(515, divisors=(1030,)), Constants.posscale(1542, divisors=(1030,))]
    # Remove skys that are off-screen
    sky_remove = []

    def __init__(self, menu: Menu):
        super().__init__(menu)

    def run_menu_background(self, screen: pygame.Surface, menu: Menu):
        """Receives control first, blits menu BG animation"""
        self.sky_remove = []

        # Find off-screen skies and draw skies
        for idx, sky in enumerate(self.skys):
            screen.blit(self.MENU_SKY_IMAGE, (int(sky - Constants.posscale(515, divisors=(1030,))), 0))
            self.skys[idx] -= 1
            if sky <= Constants.posscale(-515, divisors=(1030,)):
                # 1 is subtracted to compensate for subtracting the 1 above
                self.sky_remove.append(sky - 1)

        # remove skys that need removing and adds a new sky to continue the loop
        for sky in self.sky_remove:
            if sky in self.skys:
                self.skys.remove(sky)
                self.skys.append(Constants.posscale(1533, divisors=(1030,)))

        # Draw foreground
        screen.blit(self.MENU_FOREGROUND_IMAGE, Constants.cscale(0, 0))

    @abstractmethod
    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        """Menu screen functionality core and event processing"""

    def run(self, screen: pygame.Surface, menu: Menu):
        self.run_menu_background(screen, menu)
        self.run_menu_foreground(screen, menu)

    def do_persist(self) -> bool: return True
