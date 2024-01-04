import pygame
import Constants
import Menu
import Sprite


class ShadowManager(Sprite.Object):
    def __init__(self, lifetime, z_order, tags):
        super().__init__(lifetime, z_order, tags)

    def update(self, menu: Menu):
        pass

    def render(self, menu: Menu, screen: pygame.Surface):
        pass
