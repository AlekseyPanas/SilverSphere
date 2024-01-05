import math
import pygame
import heapq
from dataclasses import dataclass
import functools


@dataclass
@functools.total_ordering
class RenderData:
    """Stores data passed to a renderer for a singular sprite
    is_top_left: indicates if pos refers to top left corner. If false, pos is the center
    """
    z_order: float
    surf: pygame.Surface | None
    pos: tuple[int, int]
    is_top_left: bool

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

            if rend_dat.surf is not None:
                if rend_dat.is_top_left:
                    r = rend_dat.surf.get_rect(topleft=rend_dat.pos)
                else:
                    r = rend_dat.surf.get_rect(center=rend_dat.pos)

                game_surf.blit(rend_dat.surf, r, special_flags=pygame.BLEND_ALPHA_SDL2)
