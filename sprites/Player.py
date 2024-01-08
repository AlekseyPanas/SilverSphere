from __future__ import annotations
import pygame
import Menu
from game.Renderers import RenderData
from sprites import Sprite
from sprites import Box
from sprites.Vortex import Vortex
from sprites.InflateSurface import get_splash, SplashTypes
from managers.Managers import PreAsset, AnimationPreAsset, ASSET_LOADER, register_assets
from Constants import spritesheet2frames, path2asset, is_pos_eq
import Constants
from managers import GameManager
from game import SpritesManager
import math
import time


@register_assets(ASSET_LOADER)
class Player(Sprite.Sprite):
    ANIM_INTERMEDIATES = 1

    # Player Animation images
    PLAYER_IMAGE: pygame.Surface = PreAsset(path2asset("images/Silver Ball.png"), (51, 51))
    PLAYER_UP_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Silver Up.png"), (51, 51), True, (4, 1), ANIM_INTERMEDIATES)
    PLAYER_DOWN_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Silver Ball Down.png"), (51, 51), True, (4, 1), ANIM_INTERMEDIATES)
    PLAYER_RIGHT_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Silver Right.png"), (51, 51), True, (4, 1), ANIM_INTERMEDIATES)
    PLAYER_LEFT_IMAGE: list[pygame.Surface] = AnimationPreAsset(path2asset("images/Silver Left.png"), (51, 51), True, (4, 1), ANIM_INTERMEDIATES)

    # Ball shadow
    BALL_SHADOW_IMAGE: pygame.Surface = PreAsset(path2asset("images/ball shadow.png"), (57, 30))

    SHADOW_SHIFT = (-20, 8)

    def __init__(self, lifetime: int | None, z_order: float, coords: tuple[int, int]):
        """
        :param lifetime: For temporary surfaces. Decremented manually in manager. None for infinite life
        :param z_order: For ordering in visual layers
        :param coords: player start position
        """
        super().__init__(lifetime, z_order)

        # position and grid coords
        self.coords = coords
        self.pos = list(Sprite.Sprite.get_center_from_coords(self.coords))

        # Key press stack for controlling ball
        self.STACK = Constants.Stack()

        # Load animations
        self.image = self.PLAYER_IMAGE
        self.img_l = self.PLAYER_LEFT_IMAGE
        self.img_r = self.PLAYER_RIGHT_IMAGE
        self.img_u = self.PLAYER_UP_IMAGE
        self.img_d = self.PLAYER_DOWN_IMAGE
        self.__num_frames = len(self.PLAYER_LEFT_IMAGE)

        # Image and Animation info
        self.time = 0
        # When moving, changes current image to the animation image for the corresponding direction of movement
        self.current_image = self.img_l
        self.current_index = 0

        # state
        self.state = "static"
        # list holding info on whether or not there are boxes in either of the 4 directions of the cube
        self.near_boxes = [None for x in range(4)]

        # used to track movement
        self.move_count = 0
        self.speed = 6

        # Run-Once variable for setting box state
        self.set_box_state = False

    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        self.event_handler(menu)  # Registers user keypresses
        self.animate()  # Updates animation if in motion

        # Update coordinate location on game grid
        self.coords = ((self.pos[0] - 25) / 50, (self.pos[1] - 25) / 50)

        # if not moving, detects button presses. When button pressed down, set animation image and set corresponding
        # state. Calls pre-detect to see if you are allowed to move in a certain direction (nothing blocking like iron
        # boxes or the map border... etc)
        if self.state == "static":
            detect = self.pre_detect(game_manager, sprite_manager)
            if self.STACK.peek() == 'r' and detect[0]:
                self.state = "r"
                self.current_image = self.img_r
            elif self.STACK.peek() == 'l' and detect[1]:
                self.state = "l"
                self.current_image = self.img_l
            elif self.STACK.peek() == 'u' and detect[2]:
                self.state = "u"
                self.current_image = self.img_u
            elif self.STACK.peek() == 'd' and detect[3]:
                self.state = "d"
                self.current_image = self.img_d
        # Moving function called continuously
        self.move(game_manager, sprite_manager)

        # Smooth drowning
        if self.state == "drown" and self.z_order > Sprite.ZHeights.UNDERWATER_OBJECT_HEIGHT:
            self.z_order -= Constants.DROWN_SPEED
            if self.z_order <= Sprite.ZHeights.UNDERWATER_OBJECT_HEIGHT:
                self.z_order = Sprite.ZHeights.UNDERWATER_OBJECT_HEIGHT
                sprite_manager.add_sprite(get_splash(Constants.cscale(*self.pos), SplashTypes.SPHERE_SMALL))
                sprite_manager.add_sprite(get_splash(Constants.cscale(*self.pos), SplashTypes.SPHERE_BIG))

    def render(self, menu: Menu, sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData | None:
        s: pygame.Surface | None = None

        # When stationary
        if self.state == "static" or self.state == 'drown':
            s = self.image

        # moving animation
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            s = self.current_image[self.current_index]

        return RenderData(self.z_order, self.get_drown_scale(self.z_order, s),
                          s.get_rect(center=Constants.cscale(*self.pos)))

    @staticmethod
    def get_drown_scale(zorder: float, surf: pygame.Surface):
        """If in water, return scaled surface based on zorder"""
        # Ball gets slightly smaller if drowned
        if zorder < Sprite.ZHeights.ON_GROUND_OBJECT_HEIGHT:
            diff = (Sprite.ZHeights.ON_GROUND_OBJECT_HEIGHT - zorder) / 15
            return pygame.transform.smoothscale(surf, tuple(i * (1 - (diff * 0.4)) for i in surf.get_size()))
        return surf

    def get_shadow(self) -> tuple[pygame.Surface, tuple[float, float]] | None:
        return self.get_drown_scale(self.z_order, self.BALL_SHADOW_IMAGE.copy()), \
            (self.pos[0] + self.SHADOW_SHIFT[0], self.pos[1] + self.SHADOW_SHIFT[1])

    def animate(self):
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            self.current_index = int((self.time % (6 * self.__num_frames)) // 6)
            self.time += 0.95 * (self.ANIM_INTERMEDIATES + 1)

        # # For water shadow testing
        #self.z_order = self.__zorder_copy + 3 + 3 * math.sin(time.time())

    def event_handler(self, menu: Menu):
        """Keeps track of user inputs"""
        for event in menu.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.STACK.push("r")
                elif event.key == pygame.K_LEFT:
                    self.STACK.push("l")
                elif event.key == pygame.K_DOWN:
                    self.STACK.push("d")
                elif event.key == pygame.K_UP:
                    self.STACK.push("u")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.STACK.yank("r")
                elif event.key == pygame.K_LEFT:
                    self.STACK.yank("l")
                elif event.key == pygame.K_DOWN:
                    self.STACK.yank("d")
                elif event.key == pygame.K_UP:
                    self.STACK.yank("u")

    def move(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # If any directional state is the current state, then run the code
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            diff = 50 - self.move_count
            # Moves ball continuously in direction corresponding to the state
            # If there is a box in the direction you are moving, set the state of the box to move in the corresponding
            # direction. The set_box_state is a
            # run once variable to make the state be set only once until you move again.
            if self.state == "r":
                if not self.set_box_state and not self.near_boxes[0] is None:
                    self.set_box_state = True
                    self.near_boxes[0].state = 'r'
                if diff < self.speed:
                    self.pos[0] = round(self.pos[0] + diff)
                else:
                    self.pos[0] += self.speed
            elif self.state == "l":
                if not self.set_box_state and not self.near_boxes[1] is None:
                    self.set_box_state = True
                    self.near_boxes[1].state = 'l'
                if diff < self.speed:
                    self.pos[0] = round(self.pos[0] - diff)
                else:
                    self.pos[0] -= self.speed
            elif self.state == "u":
                if not self.set_box_state and not self.near_boxes[2] is None:
                    self.set_box_state = True
                    self.near_boxes[2].state = 'u'
                if diff < self.speed:
                    self.pos[1] = round(self.pos[1] - diff)
                else:
                    self.pos[1] -= self.speed
            elif self.state == "d":
                if not self.set_box_state and not self.near_boxes[3] is None:
                    self.set_box_state = True
                    self.near_boxes[3].state = 'd'
                if diff < self.speed:
                    self.pos[1] = round(self.pos[1] + diff)
                else:
                    self.pos[1] += self.speed
            # Increment count
            self.move_count += self.speed
            # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
            if self.move_count >= 50:
                self.state = "static"
                self.move_count = 0
                # Updates Coords and runs post-detect
                self.coords = [(self.pos[0] - 25) / 50, (self.pos[1] - 25) / 50]
                self.post_detect(game_manager, sprite_manager)

    def pre_detect(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        # right, left, up, down
        allowed_movement = [True for x in range(4)]
        self.near_boxes = [None for x in range(4)]
        self.set_box_state = False
        # Detects if the end of the map is in any direction of the player
        if self.coords[0] == 19:
            allowed_movement[0] = False
        elif self.coords[0] == 0:
            allowed_movement[1] = False
        if self.coords[1] == 11:
            allowed_movement[3] = False
        elif self.coords[1] == 0:
            allowed_movement[2] = False

        # Detects metal boxes
        if allowed_movement[0] and game_manager.get_layout()[int(self.coords[1])][int(self.coords[0]) + 1] == 'B':
            allowed_movement[0] = False
        if allowed_movement[1] and game_manager.get_layout()[int(self.coords[1])][int(self.coords[0]) - 1] == 'B':
            allowed_movement[1] = False
        if allowed_movement[2] and game_manager.get_layout()[int(self.coords[1]) - 1][int(self.coords[0])] == 'B':
            allowed_movement[2] = False
        if allowed_movement[3] and game_manager.get_layout()[int(self.coords[1]) + 1][int(self.coords[0])] == 'B':
            allowed_movement[3] = False

        # Detects boxes that aren't in the water
        # If the box is not able to be pushed in a certain direction
        # (box.detect() returns that info) then allowed movement is set to false for that direction
        for box in sprite_manager.get_groups([Box.Box, Box.IceCube]):
            if not box.state == 'drown':
                box_detect = box.detect(game_manager, sprite_manager)
                if allowed_movement[0] and is_pos_eq(box.coords, [self.coords[0] + 1, self.coords[1]]):
                    self.near_boxes[0] = box
                    if not box_detect[0]:
                        allowed_movement[0] = False
                if allowed_movement[1] and is_pos_eq(box.coords, [self.coords[0] - 1, self.coords[1]]):
                    self.near_boxes[1] = box
                    if not box_detect[1]:
                        allowed_movement[1] = False
                if allowed_movement[2] and is_pos_eq(box.coords, [self.coords[0], self.coords[1] - 1]):
                    self.near_boxes[2] = box
                    if not box_detect[2]:
                        allowed_movement[2] = False
                if allowed_movement[3] and is_pos_eq(box.coords, [self.coords[0], self.coords[1] + 1]):
                    self.near_boxes[3] = box
                    if not box_detect[3]:
                        allowed_movement[3] = False

        # Returns an array which says whether movement in a certain direction is allowed
        # [Right,Left,Up,Down]
        return allowed_movement

    def set_drown(self):
        self.state = 'drown'

    def post_detect(self, game_manager: GameManager.GameManager, sprite_manager: SpritesManager.GroupSpritesManager):
        vortex: Vortex = sprite_manager.get_single(Vortex)

        # detects if player is standing on water and sets state to drown as well as starts reset timer if on water
        if game_manager.get_layout()[int(self.coords[1])][int(self.coords[0])] == 'W':
            self.set_drown()

        # Detects if on vortex
        elif is_pos_eq(vortex.coords, self.coords) and vortex.state == 'stationary':
            # sets the vortex to close
            vortex.set_image = False
            vortex.state = 'close'
            vortex.player_in = True
            # State drown to make player disappear under the tiles
            self.kill = True
            # starts timer to open post level menu
            self.z_order = Sprite.ZHeights.UNDERWATER_OBJECT_HEIGHT
