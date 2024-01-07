import math
import pygame
import heapq
from dataclasses import dataclass
import functools


@dataclass
@functools.total_ordering
class RenderData:
    """Stores data passed to a renderer for a singular sprite
    is_top_left: indicates if pos refers to top left corner. If false, pos is the center.
    Pos must be given in resolution-scaled coordinates
    """
    z_order: float
    surf: pygame.Surface
    rect: pygame.Rect

    def __eq__(self, other): return False
    def __lt__(self, other): return True


class ZHeapRenderer:
    """Renders a level surface by using a heap for z-order"""
    def __init__(self):
        self.__surface_heap: list[tuple[float, RenderData]] = []

    def add_to_frame(self, render_data: RenderData):
        """Register a positioned surface with a particular z_order to be drawn next frame"""
        heapq.heappush(self.__surface_heap, (render_data.z_order, render_data))

    def render_frame(self, game_surf: pygame.Surface):
        """Clears the heap and renders the surface"""
        while len(self.__surface_heap):
            z, rend_dat = heapq.heappop(self.__surface_heap)

            game_surf.blit(rend_dat.surf, rend_dat.rect, special_flags=pygame.BLEND_ALPHA_SDL2)
