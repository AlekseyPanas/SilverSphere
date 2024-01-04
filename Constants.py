import pygame
import math
import pathlib
import sys
import pathlib
pygame.init()

SCREEN_SIZE = (1030, 700)
#SCREEN_SIZE = (515, 350)
#SCREEN_SIZE = (824, 560)
#SCREEN_SIZE = (2060, 1400)

ASSET_PATH = pathlib.Path(sys.argv[0]).parent.joinpath("assets")


def path2asset(subpath: str):
    return ASSET_PATH.joinpath(pathlib.Path(subpath))


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


# FONTS
def get_impact(size):
    return pygame.font.SysFont("Impact", size)


def get_arial(size):
    return pygame.font.SysFont("Arial", size)


def get_sans(size):
    return pygame.font.Font(pathlib.Path(__file__).parent.joinpath("assets/BebasNeue-Regular.ttf"), size)


BIGBOI_FONT = pygame.font.SysFont("Comic Sans", int(0.045 * SCREEN_SIZE[0]))

#SCREEN_UPDATE_RECT = cscale(15, 15, 1000, 685)
