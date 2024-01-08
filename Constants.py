import pygame
import math
import pathlib
import sys
import pathlib
pygame.init()

DROWN_SPEED = 0.6  # zorder subtraction per tick for drowning object

#SCREEN_SIZE = (1030, 700)
#SCREEN_SIZE = (515, 350)
SCREEN_SIZE = (824, 560)
#SCREEN_SIZE = (2060, 1400)

GRID_DIMS = (20, 12)

ROOT_PATH = pathlib.Path(sys.argv[0]).parent
ASSET_PATH = ROOT_PATH.joinpath("assets")


def path2asset(subpath: str):
    return ASSET_PATH.joinpath(pathlib.Path(subpath))


def path2file(subpath_from_root: str):
    return ROOT_PATH.joinpath(pathlib.Path(subpath_from_root))


def distance(a, b):
    return math.sqrt((b[1] - a[1]) ** 2 + (b[0] - a[0]) ** 2)


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def yank(self, item):
        if item in self.items:
            self.items.remove(item)

    def peek(self):
        if len(self.items):
            return self.items[-1]
        else:
            return ""

    def size(self):
        return len(self.items)


def is_pos_eq(pos1: tuple | list, pos2: tuple | list):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]


def cscale(*coordinate, divisors=(1030, 700)):
    """Rounded re-scaling of values from provided resolution to current"""
    if len(coordinate) > 1:
        return tuple([round(coordinate[x] / divisors[x % 2] * SCREEN_SIZE[x % 2]) for x in range(len(coordinate))])
    else:
        return round(coordinate[0] / divisors[0] * SCREEN_SIZE[0])


def posscale(*coordinate, divisors=(1030, 700)):
    """float re-scaling of values from provided resolution to current"""
    if len(coordinate) > 1:
        return tuple([coordinate[x] / divisors[x % 2] * SCREEN_SIZE[x] for x in range(len(coordinate))])
    else:
        return coordinate[0] / divisors[0] * SCREEN_SIZE[0]


def scale_surfaces(surfs: list[pygame.Surface]):
    """Given multiple surfaces in WORLD coordinates (1030, 700), scale them to current resolution"""
    return [pygame.transform.smoothscale(s, cscale(*s.get_size())).convert_alpha() for s in surfs]


def clipper_from_surface(surf: pygame.Surface, threshold=127) -> pygame.Surface:
    """Return a surface which is white for all transparent pixels in surf, and transparent
    where surf isn't. This is useful with RGBA_SUB blend mode to clip other surfaces to be
    the shape of the provided surf
    :param surf: Surface to get clipper of
    :param threshold: alpha thresh to determine whether pixel is clipped or not
    """
    return pygame.mask.from_surface(surf, threshold).to_surface(setcolor=(0, 0, 0, 0), unsetcolor=(255, 255, 255, 255))


def spritesheet2frames(spritesheet: pygame.Surface, frame_dims_xy: tuple[int, int],
                       intermediates=0, loop: bool = True) -> list[pygame.Surface]:
    """
    Return sequence of frame surfaces from an animation spritesheet. The spritesheet is assumed
    to organize frames left to right top to bottom (i.e. one row finishes, the next frame is found
    at the beginning of the next row)
    :param spritesheet: surface representing the spritesheet
    :param frame_dims_xy: Number of frame columns and rows
    :param intermediates: Number of frames to add between each frame where the frames are alpha blended
    :param loop: Determines if the final intermediate frames fade out or fade back into the first frame
    :return:
    """
    frames: list[pygame.Surface] = []
    final_frames: list[pygame.Surface] = []

    frame_size = (spritesheet.get_size()[0] // frame_dims_xy[0],
                  spritesheet.get_size()[1] // frame_dims_xy[1])

    # Extract frames
    for row in range(frame_dims_xy[1]):
        for col in range(frame_dims_xy[0]):
            frame = pygame.Surface(frame_size, pygame.SRCALPHA, depth=32).convert_alpha()
            frame.blit(spritesheet, (-col * frame_size[0], -row * frame_size[1]))
            frames.append(frame.convert_alpha())

    # Compute intermediates
    alpha_increment = 255 / (intermediates + 1)
    for f in range(len(frames)):
        if intermediates == 0: final_frames.append(frames[f])
        for i in range(1, intermediates + 1):
            cur_alpha = alpha_increment * i

            frame = pygame.Surface(frame_size, pygame.SRCALPHA, depth=32).convert_alpha()
            f_prev = frames[f].copy()

            #f_prev.fill((0, 0, 0, max(0, i - (intermediates // 2)) * 2 * alpha_increment), special_flags=pygame.BLEND_RGBA_SUB)

            if loop or f > 0:
                f_prev_prev = frames[(f-1) % len(frames)].copy()
                f_prev_prev.fill((0, 0, 0, cur_alpha), special_flags=pygame.BLEND_RGBA_SUB)
                frame.blit(f_prev_prev, (0, 0))

            if not loop and f == len(frames) - 1:
                f_prev.fill((0, 0, 0, cur_alpha), special_flags=pygame.BLEND_RGBA_SUB)
            frame.blit(f_prev, (0, 0))

            if loop or f < len(frames) - 1:
                f_next = frames[(f+1) % len(frames)].copy()
                f_next.fill((0, 0, 0, 255 - cur_alpha), special_flags=pygame.BLEND_RGBA_SUB)
                frame.blit(f_next, (0, 0))

            final_frames.append(frame.convert_alpha())

    return final_frames


# FONTS
def get_impact(size):
    return pygame.font.SysFont("Impact", size)


def get_arial(size):
    return pygame.font.SysFont("Arial", size)


def get_sans(size):
    return pygame.font.Font(path2asset("fonts/BebasNeue-Regular.ttf"), size)


BIGBOI_FONT = pygame.font.SysFont("Comic Sans", int(0.045 * SCREEN_SIZE[0]))
