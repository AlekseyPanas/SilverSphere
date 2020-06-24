import pygame
pygame.init()

SCREEN_SIZE = (1030, 700)
#SCREEN_SIZE = (515, 350)
#SCREEN_SIZE = (824, 560)
#SCREEN_SIZE = (2060, 1400)

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


# Scales a set of coordinates to the current screen size based on a divisor factor
def cscale(*coordinate, divisors=(1030, 700)):
    if len(coordinate) > 1:
        return tuple([round(coordinate[x] / divisors[x % 2] * SCREEN_SIZE[x % 2]) for x in range(len(coordinate))])
    else:
        return round(coordinate[0] / divisors[0] * SCREEN_SIZE[0])


# Scales a set of coordinates to the current screen size based on a divisor factor. Doesn't return integers
def posscale(*coordinate, divisors=(1030, 700)):
    if len(coordinate) > 1:
        return tuple([coordinate[x] / divisors[x % 2] * SCREEN_SIZE[x] for x in range(len(coordinate))])
    else:
        return coordinate[0] / divisors[0] * SCREEN_SIZE[0]


def convert():
    global PLAYER_IMAGE, PLAYER_LEFT_IMAGE, PLAYER_RIGHT_IMAGE, PLAYER_DOWN_IMAGE, PLAYER_UP_IMAGE, FLOOR_TILE_IMAGE, \
        IRON_TILE_IMAGE, VORTEX_TILE_IMAGE, VORTEX_CLOSE_IMAGE, VORTEX_OPEN_IMAGE, ICE_X_TILE_IMAGE, BOX_X_TILE_IMAGE, \
        BOX_IMAGE, ICE_IMAGE, BORDER_IMAGE, WATER_IMAGE, MARBLE_IMAGE, WATER_SHADOW_IMAGE, BALL_SHADOW_IMAGE, \
        MENU_FOREGROUND_IMAGE, MENU_SKY_IMAGE, EXIT_ICON_IMAGE, EXPLOSION_IMAGE, PLAY_BUTTON_IMAGE, \
        INLEVEL_PLAY_BUTTON_IMAGE, NEXTLVL_BUTTON_IMAGE, LEVELS_BUTTON_IMAGE, LOCK_IMAGE

    PLAYER_IMAGE = PLAYER_IMAGE.convert_alpha()
    PLAYER_LEFT_IMAGE = PLAYER_LEFT_IMAGE.convert_alpha()
    PLAYER_RIGHT_IMAGE = PLAYER_RIGHT_IMAGE.convert_alpha()
    PLAYER_UP_IMAGE = PLAYER_UP_IMAGE.convert_alpha()
    PLAYER_DOWN_IMAGE = PLAYER_DOWN_IMAGE.convert_alpha()

    FLOOR_TILE_IMAGE = FLOOR_TILE_IMAGE.convert_alpha()
    IRON_TILE_IMAGE = IRON_TILE_IMAGE.convert_alpha()

    VORTEX_TILE_IMAGE = VORTEX_TILE_IMAGE.convert_alpha()
    VORTEX_OPEN_IMAGE = VORTEX_OPEN_IMAGE.convert_alpha()
    VORTEX_CLOSE_IMAGE = VORTEX_CLOSE_IMAGE.convert_alpha()
    ICE_X_TILE_IMAGE = ICE_X_TILE_IMAGE.convert_alpha()
    BOX_X_TILE_IMAGE = BOX_X_TILE_IMAGE.convert_alpha()

    BOX_IMAGE = BOX_IMAGE.convert_alpha()
    ICE_IMAGE = ICE_IMAGE.convert_alpha()

    BORDER_IMAGE = BORDER_IMAGE.convert_alpha()
    WATER_IMAGE = WATER_IMAGE.convert_alpha()
    MARBLE_IMAGE = MARBLE_IMAGE.convert_alpha()
    WATER_SHADOW_IMAGE = WATER_SHADOW_IMAGE.convert_alpha()
    BALL_SHADOW_IMAGE = BALL_SHADOW_IMAGE.convert_alpha()
    MENU_FOREGROUND_IMAGE = MENU_FOREGROUND_IMAGE.convert_alpha()
    MENU_SKY_IMAGE = MENU_SKY_IMAGE.convert_alpha()
    EXIT_ICON_IMAGE = EXIT_ICON_IMAGE.convert_alpha()

    EXPLOSION_IMAGE = EXPLOSION_IMAGE.convert_alpha()

    PLAY_BUTTON_IMAGE = PLAY_BUTTON_IMAGE.convert_alpha()
    INLEVEL_PLAY_BUTTON_IMAGE = INLEVEL_PLAY_BUTTON_IMAGE.convert_alpha()
    NEXTLVL_BUTTON_IMAGE = NEXTLVL_BUTTON_IMAGE.convert_alpha()
    LEVELS_BUTTON_IMAGE = LEVELS_BUTTON_IMAGE.convert_alpha()

    LOCK_IMAGE = LOCK_IMAGE.convert_alpha()

# Player Animation images
PLAYER_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/Silver Ball.png"), cscale(51, 51))
PLAYER_UP_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/Silver Up.png"), cscale(204, 51))
PLAYER_DOWN_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/Silver Ball Down.png"), cscale(204, 51))
PLAYER_RIGHT_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/Silver Right.png"), cscale(204, 51))
PLAYER_LEFT_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/Silver Left.png"), cscale(204, 51))

# Tile Images
FLOOR_TILE_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/floor.png"), (50, 50))
IRON_TILE_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/iron.png"), (50, 50))

VORTEX_TILE_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/vortex anim.png"), cscale(770, 70))
VORTEX_OPEN_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/vortex open.png"), cscale(630, 70))
VORTEX_CLOSE_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/vortex close.png"), cscale(630, 70))
ICE_X_TILE_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/Xice.png"), (1, 1))
BOX_X_TILE_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/Xbox.png"), (1, 1))

# Box and Ice Entity Images
BOX_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/Wooden crate.png"), (1, 1))
ICE_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/icecube.png"), (1, 1))

# Border Image
BORDER_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/border.png"), (1, 1))
WATER_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/water.png"), cscale(1000, 600))
MARBLE_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/marble background.png"), cscale(1000, 600))
WATER_SHADOW_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/shadow 2.png"), (100, 100))
BALL_SHADOW_IMAGE = pygame.transform.smoothscale(pygame.image.load("assets/images/ball shadow.png"), cscale(57, 30))
MENU_FOREGROUND_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/title screen.png"), cscale(1030, 700))
MENU_SKY_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/cloud.png"), cscale(1030, 700))
EXIT_ICON_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/X.png"), (1, 1))

LOCK_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/lock_icon.png"), cscale(50, 50))

EXPLOSION_IMAGE = pygame.transform.scale(pygame.image.load("assets/images/explosion.png"), (1, 1))

# Button Images
PLAY_BUTTON_IMAGE = pygame.image.load("assets/images/title play.png")
INLEVEL_PLAY_BUTTON_IMAGE = pygame.image.load("assets/images/play.png")
NEXTLVL_BUTTON_IMAGE = pygame.image.load("assets/images/nxtlvl.png")
LEVELS_BUTTON_IMAGE = pygame.image.load("assets/images/level select button.png")


# FONTS
def get_impact(size):
    return pygame.font.SysFont("Impact", size)


def get_arial(size):
    return pygame.font.SysFont("Arial", size)


def get_sans(size):
    return pygame.font.SysFont("Comic Sans", size)


BIGBOI_FONT = pygame.font.SysFont("Comic Sans", int(0.045 * SCREEN_SIZE[0]))
