import math
import pygame
import heapq


class ZHeapRenderer:
    """Renders a level surface by using a heap for z-order"""
    def __init__(self):
        self.__surface_heap: list = []

    def add_to_frame(self, surf: pygame.Surface, center: tuple[int, int], z_order: float):
        """Register a positioned surface with a particular z_order to be drawn next frame"""
        heapq.heappush(self.__surface_heap, (z_order, surf, center))

    def render_frame(self, game_surf: pygame.Surface):
        """Clears the heap and renders the surface"""
        while len(self.__surface_heap):
            z, surf, center = heapq.heappop(self.__surface_heap)
            surf: pygame.Surface

            game_surf.blit(surf, surf.get_rect(center=center), special_flags=pygame.BLEND_ALPHA_SDL2)
