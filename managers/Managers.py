from __future__ import annotations
import Menu
import pygame
import Constants
from Constants import cscale, spritesheet2frames
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
                if isinstance(asset, AnimationPreAsset):
                    setattr(obj, k, self.convert_animation_preasset(asset))
                else:
                    setattr(obj, k, self.convert_preasset(asset))

    @staticmethod
    def convert_preasset(asset: PreAsset) -> pygame.Surface:
        """Transform and convert PreAsset to a pygame surface"""
        if isinstance(asset.path, pygame.Surface): img = asset.path
        else: img = pygame.image.load(asset.path)

        if asset.size is None:
            return img.convert_alpha()
        else:
            s = Constants.cscale(*asset.size) if asset.do_resolution_scale else asset.size
            return pygame.transform.smoothscale(img, s).convert_alpha()

    @staticmethod
    def convert_animation_preasset(asset: AnimationPreAsset):
        """Parse spritesheet and scale each frame"""
        if isinstance(asset.path, pygame.Surface): img = asset.path
        else: img = pygame.image.load(asset.path)

        frames = spritesheet2frames(img, asset.frame_dims, asset.intermediates, asset.loop)
        parsed_frames = []
        for f in frames:
            if asset.size is None:
                parsed_frames.append(f.convert_alpha())
            else:
                s = Constants.cscale(*asset.size) if asset.do_resolution_scale else asset.size
                parsed_frames.append(pygame.transform.smoothscale(f, s).convert_alpha())
        return parsed_frames


ASSET_LOADER = DelayedAssetLoader()


@dataclass
class PreAsset:
    """
    do_resolution_scale will compute the scaled size and then transform
    :param path: Can be a string to a file or a ready surface
    """
    path: str | pygame.Surface
    size: tuple[int, int] = None
    do_resolution_scale: bool = True


@dataclass
class AnimationPreAsset(PreAsset):
    """Computes spritesheet and scales each frame to specified size"""
    frame_dims: tuple[int, int] = (1, 1)
    intermediates: int = 0
    loop: bool = True


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










