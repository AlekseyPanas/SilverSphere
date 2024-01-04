from __future__ import annotations
import Menu
import pygame
import Constants
from Constants import cscale
import Button
from abc import abstractmethod
from dataclasses import dataclass


class DelayedAssetLoader:
    def __init__(self):
        self.__classes = []

    def register(self, obj_type: type):
        """Append attributes for delayed loading"""
        self.__classes.append(obj_type)

    def load(self):
        """Load the assets"""
        for obj in self.__classes:
            for k in [k for k in obj.__dict__ if isinstance(obj.__dict__[k], PreAsset)]:  # Loop through PreAsset attributes
                asset = obj.__dict__[k]
                if asset.size is None:
                    setattr(obj, k, pygame.image.load(asset.path).convert_alpha())
                else:
                    setattr(obj, k, pygame.transform.smoothscale(pygame.image.load(asset.path),
                                                                 Constants.cscale(*asset.size)).convert_alpha())


ASSET_LOADER = DelayedAssetLoader()


@dataclass
class PreAsset:
    path: str
    size: tuple[int, int] = None


def register_assets(asset_loader: DelayedAssetLoader):
    """Decorator for loading python image assets and converting them when defined as static
    variables in a class. The class is registered with a delayed loader which can then be called
    to inject the assets later"""
    def dec(obj: type):
        asset_loader.register(obj)
        return obj
    return dec


class Manager:
    """Abstract class for a game screen"""
    def __init__(self, menu: Menu, **kwargs): pass

    @abstractmethod
    def run(self, screen: pygame.Surface, menu: Menu):
        """Given the screen and the parent Menu manager, perform one frame of execution"""

    def do_persist(self) -> bool:
        """Return if this instance should be reused on state change"""










