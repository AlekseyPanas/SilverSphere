from __future__ import annotations
import pygame
import copy
import Menu
from abc import abstractmethod
from game.Renderers import RenderData
from sprites.Sprite import Sprite
from managers.Managers import PreAsset, ASSET_LOADER, register_assets
from Constants import spritesheet2frames
import Constants
from managers import GameManager
from game import SpritesManager


@register_assets(ASSET_LOADER)
class Player(Sprite):
    # Player Animation images
    PLAYER_IMAGE: pygame.Surface = PreAsset("assets/images/Silver Ball.png", (51, 51))
    PLAYER_UP_IMAGE: pygame.Surface = PreAsset("assets/images/Silver Up.png", (204, 51))
    PLAYER_DOWN_IMAGE: pygame.Surface = PreAsset("assets/images/Silver Ball Down.png", (204, 51))
    PLAYER_RIGHT_IMAGE: pygame.Surface = PreAsset("assets/images/Silver Right.png", (204, 51))
    PLAYER_LEFT_IMAGE: pygame.Surface = PreAsset("assets/images/Silver Left.png", (204, 51))

    # Ball shadow
    BALL_SHADOW_IMAGE: pygame.Surface = PreAsset("assets/images/ball shadow.png", (57, 30))

    def __init__(self, lifetime: int | None, z_order: float, coords: tuple[int, int]):
        """
        :param lifetime: For temporary surfaces. Decremented manually in manager. None for infinite life
        :param z_order: For ordering in visual layers
        :param coords: player start position
        """
        super().__init__(lifetime, z_order)

        # position and grid coords
        self.coords = coords
        self.pos = list(Sprite.get_center_from_coords(self.coords))

        # Key press stack for controlling ball
        self.STACK = Constants.Stack()

        # Load animations
        self.image = self.PLAYER_IMAGE
        self.img_l = spritesheet2frames(self.PLAYER_LEFT_IMAGE, (4, 1), 0)
        self.img_r = spritesheet2frames(self.PLAYER_RIGHT_IMAGE, (4, 1), 0)
        self.img_u = spritesheet2frames(self.PLAYER_UP_IMAGE, (4, 1), 0)
        self.img_d = spritesheet2frames(self.PLAYER_DOWN_IMAGE, (4, 1), 0)

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
        self.coords = ((self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50)

        # if not moving, detects button presses. When button pressed down, set animation image and set corresponding
        # state. Calls pre-detect to see if you are allowed to move in a certain direction (nothing blocking like iron
        # boxes or the map border... etc)
        # if self.state == "static":
        #     detect = self.pre_detect()
        #     if self.STACK.peek() == 'r' and detect[0]:
        #         self.state = "r"
        #         self.current_image = self.img_r
        #     elif self.STACK.peek() == 'l' and detect[1]:
        #         self.state = "l"
        #         self.current_image = self.img_l
        #     elif self.STACK.peek() == 'u' and detect[2]:
        #         self.state = "u"
        #         self.current_image = self.img_u
        #     elif self.STACK.peek() == 'd' and detect[3]:
        #         self.state = "d"
        #         self.current_image = self.img_d
        # Moving function called continuously
        #self.move()

    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData:
        # When stationary
        if self.state == "static" or self.state == 'drown':
            return RenderData(self.z_order, self.image, Constants.cscale(*self.pos), False)

        # moving animation
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            return RenderData(self.z_order, self.current_image[self.current_index],
                              Constants.cscale(*self.pos), False)

    def get_shadow(self) -> pygame.Surface | None:
        return self.BALL_SHADOW_IMAGE

    def animate(self):
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            self.current_index = int((self.time % 24) // 6)
            self.time += 0.95

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

    # def move(self):
    #     # If any directional state is the current state, then run the code
    #     if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
    #         diff = 50 - self.move_count
    #         # Moves ball continuously in direction corresponding to the state
    #         # If there is a box in the direction you are moving, set the state of the box to move in the corresponding
    #         # direction. The set_box_state is a
    #         # run once variable to make the state be set only once until you move again.
    #         if self.state == "r":
    #             if not self.set_box_state and not self.near_boxes[0] is None:
    #                 self.set_box_state = True
    #                 self.near_boxes[0].state = 'r'
    #             if diff < self.speed:
    #                 self.pos[0] = round(self.pos[0] + diff)
    #             else:
    #                 self.pos[0] += self.speed
    #         elif self.state == "l":
    #             if not self.set_box_state and not self.near_boxes[1] is None:
    #                 self.set_box_state = True
    #                 self.near_boxes[1].state = 'l'
    #             if diff < self.speed:
    #                 self.pos[0] = round(self.pos[0] - diff)
    #             else:
    #                 self.pos[0] -= self.speed
    #         elif self.state == "u":
    #             if not self.set_box_state and not self.near_boxes[2] is None:
    #                 self.set_box_state = True
    #                 self.near_boxes[2].state = 'u'
    #             if diff < self.speed:
    #                 self.pos[1] = round(self.pos[1] - diff)
    #             else:
    #                 self.pos[1] -= self.speed
    #         elif self.state == "d":
    #             if not self.set_box_state and not self.near_boxes[3] is None:
    #                 self.set_box_state = True
    #                 self.near_boxes[3].state = 'd'
    #             if diff < self.speed:
    #                 self.pos[1] = round(self.pos[1] + diff)
    #             else:
    #                 self.pos[1] += self.speed
    #         # Increment count
    #         self.move_count += self.speed
    #         # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
    #         if self.move_count >= 50:
    #             self.state = "static"
    #             self.move_count = 0
    #             # Updates Coords and runs post-detect
    #             self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
    #             self.post_detect()
    #
    # def pre_detect(self):
    #     # right, left, up, down
    #     allowed_movement = [True for x in range(4)]
    #     self.near_boxes = [None for x in range(4)]
    #     self.set_box_state = False
    #     # Detects if the end of the map is in any direction of the player
    #     if self.coords[0] == 19:
    #         allowed_movement[0] = False
    #     elif self.coords[0] == 0:
    #         allowed_movement[1] = False
    #     if self.coords[1] == 11:
    #         allowed_movement[3] = False
    #     elif self.coords[1] == 0:
    #         allowed_movement[2] = False
    #
    #     # Detects metal boxes
    #     if allowed_movement[0] and Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0]) + 1] == 'B':
    #         allowed_movement[0] = False
    #     if allowed_movement[1] and Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0]) - 1] == 'B':
    #         allowed_movement[1] = False
    #     if allowed_movement[2] and Globe.MENU.game.ground_layout[int(self.coords[1]) - 1][int(self.coords[0])] == 'B':
    #         allowed_movement[2] = False
    #     if allowed_movement[3] and Globe.MENU.game.ground_layout[int(self.coords[1]) + 1][int(self.coords[0])] == 'B':
    #         allowed_movement[3] = False
    #
    #     # Detects boxes that aren't in the water
    #     # If the box is not able to be pushed in a certain direction
    #     # (box.detect() returns that info) then allowed movement is set to false for that direction
    #     for box in Globe.MENU.game.boxes:
    #         if not box.state == 'drown':
    #             box_detect = box.detect()
    #             if allowed_movement[0] and box.coords == [self.coords[0] + 1, self.coords[1]]:
    #                 self.near_boxes[0] = box
    #                 if not box_detect[0]:
    #                     allowed_movement[0] = False
    #             if allowed_movement[1] and box.coords == [self.coords[0] - 1, self.coords[1]]:
    #                 self.near_boxes[1] = box
    #                 if not box_detect[1]:
    #                     allowed_movement[1] = False
    #             if allowed_movement[2] and box.coords == [self.coords[0], self.coords[1] - 1]:
    #                 self.near_boxes[2] = box
    #                 if not box_detect[2]:
    #                     allowed_movement[2] = False
    #             if allowed_movement[3] and box.coords == [self.coords[0], self.coords[1] + 1]:
    #                 self.near_boxes[3] = box
    #                 if not box_detect[3]:
    #                     allowed_movement[3] = False
    #
    #     # Returns an array which says whether or not movement in a certain direction is allowed
    #     # [Right,Left,Up,Down]
    #     return allowed_movement
    #
    # def set_drown(self):
    #     self.state = 'drown'
    #
    #     self.z_order = -3
    #     Globe.MENU.game.sort_needed = True
    #
    # def post_detect(self):
    #     # detects if player is standing on water and sets state to drown as well as starts reset timer if on water
    #     if Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0])] == 'W':
    #         Globe.MENU.game.reset = True
    #
    #         self.set_drown()
    #
    #     # Detects if on vortex
    #     elif Globe.MENU.game.vortex.coords == self.coords and Globe.MENU.game.vortex.state == 'stationary':
    #         # sets the vortex to close
    #         Globe.MENU.game.vortex.set_image = False
    #         Globe.MENU.game.vortex.state = 'close'
    #         # State drown to make player disappear under the tiles
    #         self.state = 'drown'
    #         # starts timer to open post level menu
    #         Globe.MENU.game.start_ending = True
    #
    #         self.z_order = -3
    #         Globe.MENU.game.sort_needed = True
