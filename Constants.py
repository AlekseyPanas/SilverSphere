import pygame
import math
import pathlib
from dataclasses import dataclass
pygame.init()

BIRTHDAY = False
SCREEN_SIZE = (1030, 700)
#SCREEN_SIZE = (515, 350)
#SCREEN_SIZE = (824, 560)
#SCREEN_SIZE = (2060, 1400)


@dataclass
class PreAsset:
    path: str
    size: tuple[int, int] = None

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


def convert():
    for g in [k for k in globals() if isinstance(globals()[k], PreAsset)]:
        if globals()[g].size is None:
            globals()[g] = pygame.image.load(globals()[g].path).convert_alpha()
        else:
            globals()[g] = pygame.transform.smoothscale(pygame.image.load(globals()[g].path),
                                                        cscale(*globals()[g].size)).convert_alpha()





# Player Animation images
PLAYER_IMAGE = PreAsset("assets/images/Silver Ball.png", (51, 51))
PLAYER_UP_IMAGE = PreAsset("assets/images/Silver Up.png", (204, 51))
PLAYER_DOWN_IMAGE = PreAsset("assets/images/Silver Ball Down.png", (204, 51))
PLAYER_RIGHT_IMAGE = PreAsset("assets/images/Silver Right.png", (204, 51))
PLAYER_LEFT_IMAGE = PreAsset("assets/images/Silver Left.png", (204, 51))

ENEMY_IMAGE = PreAsset("assets/images/Golden Ball.png", (51, 51))
ENEMY_UP_IMAGE = PreAsset("assets/images/Gold Up.png", (204, 51))
ENEMY_DOWN_IMAGE = PreAsset("assets/images/Gold Down.png", (204, 51))
ENEMY_RIGHT_IMAGE = PreAsset("assets/images/Gold Right.png", (204, 51))
ENEMY_LEFT_IMAGE = PreAsset("assets/images/Gold Left.png", (204, 51))

# Tile Images
FLOOR_TILE_IMAGE = PreAsset("assets/images/floor.png", (50, 50))
IRON_TILE_IMAGE = PreAsset("assets/images/iron.png", (50, 50))

VORTEX_TILE_IMAGE = PreAsset("assets/images/vortex anim.png", (770, 70))
VORTEX_OPEN_IMAGE = PreAsset("assets/images/vortex open.png", (630, 70))
VORTEX_CLOSE_IMAGE = PreAsset("assets/images/vortex close.png", (630, 70))
ICE_X_TILE_IMAGE = PreAsset("assets/images/Xice.png", (63, 63))
BOX_X_TILE_IMAGE = PreAsset("assets/images/Xbox.png", (63, 63))

# Box and Ice Entity Images
BOX_IMAGE = PreAsset("assets/images/Wooden crate.png", (50, 50))
ICE_IMAGE = PreAsset("assets/images/icecube.png", (50, 50))

# Border Image
BORDER_IMAGE = PreAsset("assets/images/border.png", (1030, 700))
WATER_IMAGE = PreAsset("assets/images/water.png", (1000, 600))
MARBLE_IMAGE = PreAsset("assets/images/marble background.png", (1000, 600))
WATER_SHADOW_IMAGE = PreAsset("assets/images/shadow 2.png", (100, 100))
SCALED_WATER_SHADOW_IMAGE = PreAsset("assets/images/shadow 2.png", (100, 100))
BALL_SHADOW_IMAGE = PreAsset("assets/images/ball shadow.png", (57, 30))
MENU_FOREGROUND_IMAGE = PreAsset("assets/images/title screen.png", (1030, 700))
MENU_SKY_IMAGE = PreAsset("assets/images/cloud.png", (1030, 700))
EXIT_ICON_IMAGE = PreAsset("assets/images/X.png", (50, 50))

LOCK_IMAGE = PreAsset("assets/images/lock_icon.png", (50, 50))

EXPLOSION_IMAGE = PreAsset("assets/images/explosion.png", (800, 800))

# Button Images
PLAY_BUTTON_IMAGE = PreAsset("assets/images/title play.png")
INLEVEL_PLAY_BUTTON_IMAGE = PreAsset("assets/images/play.png")
NEXTLVL_BUTTON_IMAGE = PreAsset("assets/images/nxtlvl.png")
LEVELS_BUTTON_IMAGE = PreAsset("assets/images/level select button.png")

# Birthday images
BDAY_BACKGROUND = PreAsset("assets/images/bdaybg.png", (1030, 700))
BDAY_TEXT = PreAsset("assets/images/bdaytext.png", (995, 142))
BDAY_BALLOON = PreAsset("assets/images/balloon.png", (83, 219))

# FONTS
def get_impact(size):
    return pygame.font.SysFont("Impact", size)


def get_arial(size):
    return pygame.font.SysFont("Arial", size)


def get_sans(size):
    return pygame.font.Font(pathlib.Path(__file__).parent.joinpath("assets/BebasNeue-Regular.ttf"), size)


BIGBOI_FONT = pygame.font.SysFont("Comic Sans", int(0.045 * SCREEN_SIZE[0]))

#SCREEN_UPDATE_RECT = cscale(15, 15, 1000, 685)
