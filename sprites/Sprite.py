from __future__ import annotations
import pygame
import Constants
import copy
import Menu
from abc import abstractmethod
from game.Renderers import RenderData
from managers import GameManager
from game import SpritesManager

MARBLE_HEIGHT = 0.0
UNDERWATER_HEIGHT = 1.0
WATER_HEIGHT = 1.5
GROUND_HEIGHT = 2.0
METAL_HEIGHT = 3.0


class Sprite:
    def __init__(self, lifetime: int | None, z_order: float):
        self.lifetime: int | None = lifetime
        self.kill = False

        # Draw order and height reference
        self.z_order: float = z_order

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    @staticmethod
    def get_center_from_coords(coords):
        """Gets tile center from level grid coordinates (position not scaled to resolution)"""
        return (coords[0] * 50) + 25, (coords[1] * 50) + 25

    @abstractmethod
    def update(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager):
        """Update game data of this sprite object and add/remove any sprites via sprite_manager"""

    @abstractmethod
    def render(self, menu: Menu, game_manager: GameManager.GameManager,
               sprite_manager: SpritesManager.GroupSpritesManager) -> RenderData:
        """Return object's render data"""

    @abstractmethod
    def get_shadow(self) -> pygame.Surface | None:
        """Return None if this object casts no shadow. Otherwise, return a Surface
        which represents the shadow this object would cast if it was directly on the
        ground"""


    #
    # # Enemy ball animations
    # ENEMY_IMAGE: pygame.Surface = PreAsset("assets/images/Golden Ball.png", (51, 51))
    # ENEMY_UP_IMAGE: pygame.Surface = PreAsset("assets/images/Gold Up.png", (204, 51))
    # ENEMY_DOWN_IMAGE: pygame.Surface = PreAsset("assets/images/Gold Down.png", (204, 51))
    # ENEMY_RIGHT_IMAGE: pygame.Surface = PreAsset("assets/images/Gold Right.png", (204, 51))
    # ENEMY_LEFT_IMAGE: pygame.Surface = PreAsset("assets/images/Gold Left.png", (204, 51))
    #

    #
    # # Vortex animations
    # VORTEX_TILE_IMAGE: pygame.Surface = PreAsset("assets/images/vortex anim.png", (770, 70))
    # VORTEX_OPEN_IMAGE: pygame.Surface = PreAsset("assets/images/vortex open.png", (630, 70))
    # VORTEX_CLOSE_IMAGE: pygame.Surface = PreAsset("assets/images/vortex close.png", (630, 70))
    #
    # # Box, Ice, and X images
    # BOX_IMAGE: pygame.Surface = PreAsset("assets/images/Wooden crate.png", (50, 50))
    # ICE_IMAGE: pygame.Surface = PreAsset("assets/images/icecube.png", (50, 50))
    # ICE_X_TILE_IMAGE: pygame.Surface = PreAsset("assets/images/Xice.png", (63, 63))
    # BOX_X_TILE_IMAGE: pygame.Surface = PreAsset("assets/images/Xbox.png", (63, 63))
    #
    # BORDER_IMAGE: pygame.Surface = PreAsset("assets/images/border.png", (1030, 700))  # Level Border Image

    # WATER_SHADOW_IMAGE: pygame.Surface = PreAsset("assets/images/shadow 2.png", (100, 100))  # tile shadow

    # EXPLOSION_IMAGE: pygame.Surface = PreAsset("assets/images/explosion.png", (800, 800))  # Explosion animation
    #
    # # In-level buttons
    # INLEVEL_PLAY_BUTTON_IMAGE = PreAsset("assets/images/play.png")
    # NEXTLVL_BUTTON_IMAGE = PreAsset("assets/images/nxtlvl.png")

# class StaticImage(Object):
#     def __init__(self, lifetime, z_order, tags, image, pos):
#         super().__init__(lifetime, z_order, tags)
#
#         self.image = image
#         self.pos = pos
#
#     def run_sprite(self, screen, update_lock):
#         screen.blit(self.image, Constants.cscale(*self.pos))
#
#
#
#
# class Vortex(Object):
#     def __init__(self, lifetime, z_order, tags, coords):
#         super().__init__(lifetime, z_order, tags)
#         self.coords = coords
#         self.pos = Object.get_center_from_coords(coords)
#         self.state = 'blank'
#         # Vortex animation images
#         self.open = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(9)]
#         self.close = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(9)]
#         self.stationary = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(11)]
#
#         # Blits each frame onto the respective surface of the list of animation surfaces
#         [self.open[i].blit(Constants.VORTEX_OPEN_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.open))]
#         [self.close[i].blit(Constants.VORTEX_CLOSE_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.close))]
#         [self.stationary[i].blit(Constants.VORTEX_TILE_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.stationary))]
#
#         self.current_image = None
#         # run once variable to set image
#         self.set_image = False
#
#         # animation variables   frames, and animation speed
#         self.time = 0
#         self.frames = 1
#         self.animation_speed = None
#
#     def run_sprite(self, screen, update_lock):
#         if not update_lock:
#             self.update()
#         self.draw(screen, update_lock)
#
#     def update(self):
#         if self.state == 'open' or self.state == 'close':
#             # sets image, frames, and animation speed, resets time to start animation from the beginning
#             if not self.set_image and self.state == 'close':
#                 self.current_image = self.close
#                 self.set_image = True
#                 self.frames = 9
#                 self.animation_speed = 0.35
#                 self.time = 0
#             elif not self.set_image and self.state == 'open':
#                 self.current_image = self.open
#                 self.set_image = True
#                 self.frames = 9
#                 self.animation_speed = 0.35
#                 self.time = 0
#
#         elif self.state == 'stationary':
#             if not self.set_image:
#                 self.current_image = self.stationary
#                 self.set_image = True
#                 self.frames = 11
#                 self.animation_speed = 0.28
#                 self.time = 0
#
#             # FIX THIS: Checks for boxes on open vortex and sets them to explode
#             for box in Globe.MENU.game.boxes:
#                 if box.coords == self.coords:
#                     box.kill = True
#                     Globe.MENU.game.add_sprite(Animation(-1, 12, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
#                                                          Constants.cscale(*box.pos), 74))
#
#         else:
#             self.current_image = None
#
#     def draw(self, screen, update_lock):
#         if not self.state == 'blank':
#             # increment duration and animate image
#             self.animate(screen, update_lock)
#
#     def animate(self, screen, update_lock):
#         current_index = int(self.time % self.frames)
#         if self.current_image is not None:
#             screen.blit(self.current_image[current_index], self.current_image[0].get_rect(center=Constants.cscale(*self.pos)))
#         if not update_lock:
#             self.time += self.animation_speed
#             # Checks if animation ended
#             if self.state == 'open' or self.state == 'close':
#                 if self.time > 1 and int(self.time % self.frames) == 0:
#                     if self.state == 'open':
#                         self.state = 'stationary'
#                     elif self.state == 'close':
#                         self.state = 'blank'
#                     self.set_image = False
#
#
# class Box(Object):
#     def __init__(self, lifetime, z_order, tags, coords):
#         super().__init__(lifetime, z_order, tags)
#
#         # Position and state
#         self.coords = coords
#         self.pos = list(Object.get_center_from_coords(coords))
#         self.state = "stationary"
#
#         # Used to track movement
#         self.move_count = 0
#
#         # dictionary to match strings with index
#         self.direction_dict = {'r': 0, 'l': 1, 'u': 2, 'd': 3}
#
#     def run_sprite(self, screen, update_lock):
#         self.draw(screen)
#         if not update_lock:
#             self.update()
#
#     def draw(self, screen):
#         screen.blit(Constants.BOX_IMAGE, Constants.BOX_IMAGE.get_rect(center=Constants.cscale(*self.pos)))
#
#     def update(self):
#         self.move()
#
#     def detect(self):
#         # Right,Left,Up,Down
#         allowed_movement = [True for x in range(4)]
#         # Detects if the end of the map is in any direction of the player
#         if self.coords[0] == 19:
#             allowed_movement[0] = False
#         if self.coords[0] == 0:
#             allowed_movement[1] = False
#         if self.coords[1] == 11:
#             allowed_movement[3] = False
#         if self.coords[1] == 0:
#             allowed_movement[2] = False
#
#         # Detects metal boxes
#         if allowed_movement[0] and Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0]) + 1] == 'B':
#             allowed_movement[0] = False
#         if allowed_movement[1] and Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0]) - 1] == 'B':
#             allowed_movement[1] = False
#         if allowed_movement[2] and Globe.MENU.game.ground_layout[int(self.coords[1]) - 1][int(self.coords[0])] == 'B':
#             allowed_movement[2] = False
#         if allowed_movement[3] and Globe.MENU.game.ground_layout[int(self.coords[1]) + 1][int(self.coords[0])] == 'B':
#             allowed_movement[3] = False
#
#         # Detects other boxes
#         for box in Globe.MENU.game.boxes:
#             if not box.state == 'drown':
#                 if allowed_movement[0] and box.coords == [self.coords[0] + 1, self.coords[1]]:
#                     allowed_movement[0] = False
#                 if allowed_movement[1] and box.coords == [self.coords[0] - 1, self.coords[1]]:
#                     allowed_movement[1] = False
#                 if allowed_movement[2] and box.coords == [self.coords[0], self.coords[1] - 1]:
#                     allowed_movement[2] = False
#                 if allowed_movement[3] and box.coords == [self.coords[0], self.coords[1] + 1]:
#                     allowed_movement[3] = False
#
#         # Detects Vortex in all 4 directions
#         if Globe.MENU.game.vortex.state == 'stationary':
#             if allowed_movement[0] and Globe.MENU.game.vortex.coords == [self.coords[0] + 1, self.coords[1]]:
#                 allowed_movement[0] = False
#             if allowed_movement[1] and Globe.MENU.game.vortex.coords == [self.coords[0] - 1, self.coords[1]]:
#                 allowed_movement[1] = False
#             if allowed_movement[2] and Globe.MENU.game.vortex.coords == [self.coords[0], self.coords[1] - 1]:
#                 allowed_movement[2] = False
#             if allowed_movement[3] and Globe.MENU.game.vortex.coords == [self.coords[0], self.coords[1] + 1]:
#                 allowed_movement[3] = False
#
#         # Returns an array which says whether or not movement in a certain direction is allowed
#         # [Right,Left,Up,Down]
#         return allowed_movement
#
#     def set_drown(self):
#         self.state = 'drown'
#
#         self.z_order = -4
#         Globe.MENU.game.sort_needed = True
#
#     def post_detect(self):
#         # detects if on water, and if so, makes the box's state 'drown' and sets the map tile to 'S' so the player can
#         # move on it like a normal tile and not drown
#         if Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0])] == 'W':
#             self.set_drown()
#             Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0])] = 'S'
#             Globe.MENU.game.shadows.image.blit(Constants.SCALED_WATER_SHADOW_IMAGE, Constants.cscale(self.coords[0] * 50,
#                                                                                                      self.coords[1] * 50))
#
#     def move(self):
#         # If any directional state is the current state, then run the code
#         if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
#             speed = Globe.MENU.game.player.speed
#             diff = 50 - self.move_count
#             # Moves box continuously in direction corresponding to the state
#             if self.state == "r":
#                 if diff < speed:
#                     self.pos[0] = round(self.pos[0] + diff)
#                 else:
#                     self.pos[0] += speed
#             elif self.state == "l":
#                 if diff < speed:
#                     self.pos[0] = round(self.pos[0] - diff)
#                 else:
#                     self.pos[0] -= speed
#             elif self.state == "u":
#                 if diff < speed:
#                     self.pos[1] = round(self.pos[1] - diff)
#                 else:
#                     self.pos[1] -= speed
#             elif self.state == "d":
#                 if diff < speed:
#                     self.pos[1] = round(self.pos[1] + diff)
#                 else:
#                     self.pos[1] += speed
#             # Increment count
#             self.move_count += speed
#             # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
#             if self.move_count >= 50:
#                 self.state = "stationary"
#                 self.move_count = 0
#                 # Updates Coords and runs post-detect
#                 self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
#                 self.post_detect()
#
#
# class IceCube(Box):
#     def run_sprite(self, screen, update_lock):
#         self.draw(screen)
#         if not update_lock:
#             self.update()
#
#     def draw(self, screen):
#         screen.blit(Constants.ICE_IMAGE, Constants.ICE_IMAGE.get_rect(center=Constants.cscale(*self.pos)))
#
#     def update(self):
#         self.move()
#
#     def move(self):
#         # If any directional state is the current state, then run the code
#         if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
#             speed = Globe.MENU.game.player.speed
#             diff = 50 - self.move_count
#             # Moves box continuously in direction corresponding to the state
#             if self.state == "r":
#                 if diff < speed:
#                     self.pos[0] = round(self.pos[0] + diff)
#                 else:
#                     self.pos[0] += speed
#             elif self.state == "l":
#                 if diff < speed:
#                     self.pos[0] = round(self.pos[0] - diff)
#                 else:
#                     self.pos[0] -= speed
#             elif self.state == "u":
#                 if diff < speed:
#                     self.pos[1] = round(self.pos[1] - diff)
#                 else:
#                     self.pos[1] -= speed
#             elif self.state == "d":
#                 if diff < speed:
#                     self.pos[1] = round(self.pos[1] + diff)
#                 else:
#                     self.pos[1] += speed
#             # Increment count
#             self.move_count += speed
#             # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
#             if self.move_count >= 50:
#                 self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
#                 if not self.detect()[self.direction_dict[self.state]]:
#                     self.state = "stationary"
#                     self.move_count = 0
#                     # runs post-detect
#                     self.post_detect()
#                 else:
#                     self.move_count = 0
#                     self.post_detect()
#
#
# class X_Box_Tile(Object):
#     def __init__(self, lifetime, z_order, tags, coords):
#         super().__init__(lifetime, z_order, tags)
#         self.coords = coords
#         self.pos = [(coords[0] * 50) + 40, (coords[1] * 50) + 40]
#
#     def run_sprite(self, screen, update_lock):
#         screen.blit(Constants.BOX_X_TILE_IMAGE, Constants.BOX_X_TILE_IMAGE.get_rect(center=Constants.cscale(*self.pos)))
#
#
# class X_Ice_Tile(X_Box_Tile):
#     def run_sprite(self, screen, update_lock):
#         screen.blit(Constants.ICE_X_TILE_IMAGE, Constants.BOX_X_TILE_IMAGE.get_rect(center=Constants.cscale(*self.pos)))
#
#
# '''
# ##########################
# #
# #
# #
# #
# ENEMY CLASS
# #
# #
# #
# #
# ###########################
# '''
#
#
# class Enemy(Object):
#     def __init__(self, lifetime, z_order, tags, coords, path_dir, path_dist):
#         super().__init__(lifetime, z_order, tags)
#         # Paths: [direction array ie "u", "d", "r", "l"] [distance array]
#         self.image = Constants.ENEMY_IMAGE
#         self.img_l = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
#         self.img_r = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
#         self.img_u = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
#         self.img_d = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
#
#         # Blits each frame onto the respective surface of the list of animation surfaces
#         [self.img_l[i].blit(Constants.ENEMY_LEFT_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_l))]
#         [self.img_r[i].blit(Constants.ENEMY_RIGHT_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_r))]
#         [self.img_u[i].blit(Constants.ENEMY_UP_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_u))]
#         [self.img_d[i].blit(Constants.ENEMY_DOWN_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_d))]
#
#         self.path_dir = path_dir
#         self.path_dist = path_dist
#         self.path_index = 0
#         self.path_dist_counter = 0
#
#         self.dir_dict = {"u": self.img_u, "d": self.img_d, "r": self.img_r, "l": self.img_l}
#         self.dir = self.path_dir[0]
#
#         self.current_image = self.dir_dict[self.dir]
#
#         self.time = 0
#
#         self.coords = coords
#         self.pos = list(Object.get_center_from_coords(coords))
#         self.move_count = 0
#         self.save_pos = copy.copy(self.pos)
#
#         self.speed = 6
#
#     def set_drown(self):
#         self.dir = 'drown'
#
#         self.z_order = -3
#         Globe.MENU.game.sort_needed = True
#
#     def run_sprite(self, screen, update_lock):
#         if not update_lock:
#             self.move()
#             if not self.dir == "drown":
#                 self.collisions()
#         if not self.dir == "drown":
#             self.animate(screen, update_lock)
#         else:
#             screen.blit(self.image, self.image.get_rect(center=Constants.cscale(*self.pos)))
#
#     def collisions(self):
#         sprites = copy.copy(Globe.MENU.game.boxes)
#         sprites.append(Globe.MENU.game.player)
#
#         explode_list = []
#         explode = False
#
#         for sprite in sprites:
#             dist = Constants.distance(self.pos, sprite.pos)
#             if not sprite.state == "drown":
#                 if dist < Constants.cscale(60):
#                     explode = True
#                 if dist < Constants.cscale(108):
#                     explode_list.append(sprite)
#
#         if explode:
#             for sprite in explode_list:
#                 if "player" in sprite.tags:
#                     sprite.set_drown()
#                     Globe.MENU.game.reset = True
#                 else:
#                     sprite.kill = True
#                 self.kill = True
#                 Globe.MENU.game.add_sprite(Animation(-1, 15, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
#                                                      Constants.cscale(*sprite.pos), 74))
#         if self.kill:
#             Globe.MENU.game.add_sprite(Animation(-1, 15, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
#                                                  Constants.cscale(*self.pos), 74))
#
#     def move(self):
#         if not self.dir == "drown":
#             diff = 50 - self.move_count
#             if self.dir == "u":
#                 if diff < self.speed:
#                     self.pos[1] = round(self.pos[1] - diff)
#                 else:
#                     self.pos[1] -= self.speed
#
#             elif self.dir == "d":
#                 if diff < self.speed:
#                     self.pos[1] = round(self.pos[1] + diff)
#                 else:
#                     self.pos[1] += self.speed
#
#             elif self.dir == "r":
#                 if diff < self.speed:
#                     self.pos[0] = round(self.pos[0] + diff)
#                 else:
#                     self.pos[0] += self.speed
#
#             elif self.dir == "l":
#                 if diff < self.speed:
#                     self.pos[0] = round(self.pos[0] - diff)
#                 else:
#                     self.pos[0] -= self.speed
#
#             self.move_count += self.speed
#
#             if self.move_count >= 50:
#                 self.move_count = 0
#                 self.path_dist_counter += 1
#
#                 if self.path_dist_counter == self.path_dist[self.path_index]:
#                     self.path_dist_counter = 0
#
#                     self.path_index += 1
#                     if self.path_index >= len(self.path_dir):
#                         self.path_index = 0
#
#                     self.dir = self.path_dir[self.path_index]
#                     self.current_image = self.dir_dict[self.dir]
#
#                 self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
#
#                 if Globe.MENU.game.ground_layout[int(self.coords[1])][int(self.coords[0])] == "W":
#                     self.set_drown()
#
#     def animate(self, screen, update_lock):
#         # Draw Shadow
#         screen.blit(Constants.BALL_SHADOW_IMAGE,
#                     Constants.BALL_SHADOW_IMAGE.get_rect(center=Constants.cscale(self.pos[0] + 10, self.pos[1] + 22)))
#
#         current_index = int((self.time % 24) // 6)
#         screen.blit(self.current_image[current_index], self.image.get_rect(center=Constants.cscale(*self.pos)))
#         if not update_lock:
#             self.time += 0.95
#
#
# class Animation(Object):
#     def __init__(self, lifetime, z_order, tags, sheet_dimensions, animation_speed, sheet, center, frame_count):
#         # If none is entered for lifetime, the lifetime is set to -1 iteration of the animation
#         if lifetime == -1:
#             life = frame_count * animation_speed - 1
#         else:
#             life = lifetime
#         super().__init__(life, z_order, tags)
#
#         # The dimensions of the sprite sheet by frame count (width, height)
#         self.sheet_dimensions = sheet_dimensions
#         # The amount of game ticks that should pass between each frame
#         self.animation_speed = animation_speed
#
#         self.sheet_frames_w = sheet_dimensions[0]
#         self.sheet_frames_h = sheet_dimensions[1]
#
#         # The sprite sheet image
#         self.sheet = sheet
#         # Dimensions of an individual frame
#         self.frame_width = self.sheet.get_width() / self.sheet_frames_w
#         self.frame_height = self.sheet.get_height() / self.sheet_frames_h
#
#         # Center position of the animation
#         self.pos = center
#
#         # Counts the ticks. Used for reference in the animation calculations
#         self.tick = 0
#         # Gives the current frame number
#         self.frame = 1
#         # Gets the vertical and horizontal frame coordinates to point to the current frame
#         self.frame_pos = [0, 0]
#         # Total # of frames in sheet
#         self.frame_count = frame_count
#
#         # Surface onto which the animation will be drawn
#         self.surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA, 32)
#         # Calls update once to blit the first frame and resets the tick
#         self.surface.blit(self.sheet, (0, 0))
#
#     def run_sprite(self, screen, update_lock):
#         if not update_lock:
#             self.update()
#         self.draw_sprite(screen)
#
#     def update(self):
#         # Updates
#         if self.tick % self.animation_speed == 0:
#             # Calculates the sheet position of frame
#             horizontal_pos = self.frame % self.sheet_frames_w
#             self.frame_pos = ((horizontal_pos if not horizontal_pos == 0 else 9) - 1, int(self.frame / self.sheet_frames_h - .01))
#             # Clears surface
#             self.surface.fill((255, 255, 255, 0))
#
#             # Resets frame when it finishes cycling the sheet
#             self.frame += 1
#             if self.frame > self.frame_count:
#                 self.frame = 1
#
#             # Shifts the sheet accordingly and blits the frame onto the surface
#             self.surface.blit(self.sheet,
#                               (-self.frame_pos[0] * self.frame_width, -self.frame_pos[1] * self.frame_height))
#
#         self.tick += 1
#
#     def draw_sprite(self, screen):
#         # Blits surface onto screen
#         screen.blit(self.surface, (self.pos[0] - self.frame_width / 2, self.pos[1] - self.frame_height / 2))
#
#
# # Takes a surface along with 2 scale factors (ie. .3, 1.5, 2, etc)
# # Uses the scale factors combined with the time to make the object grow on screen over time
# # Includes additional option allowing the user to fade the object
# class InflateSurface(Object):
#     def __init__(self, lifetime, z_order, tags, surface, start_scale, stop_scale, scale_time, pos, fade=False,
#                  initial_opacity=255, delay_inflation=0):
#         super().__init__(lifetime, z_order, tags)
#
#         self.surface_rect = surface.get_rect()
#
#         self.pos = pos
#
#         self.start_scale = (self.surface_rect.w * start_scale, self.surface_rect.h * start_scale)
#         self.stop_scale = (self.surface_rect.w * stop_scale, self.surface_rect.h * stop_scale)
#         self.scale_time = scale_time
#         self.current_scale = list(copy.copy(self.start_scale))
#         self.scale_increment = ((self.stop_scale[0] - self.start_scale[0]) / self.scale_time,
#                                 (self.stop_scale[1] - self.start_scale[1]) / self.scale_time)
#
#         self.surface = pygame.Surface(self.surface_rect.size, pygame.SRCALPHA, 32)
#         self.surface.blit(surface, (0, 0))
#
#         self.opacity = initial_opacity
#         self.fade_increment = (self.opacity + 1) / self.scale_time
#         self.fade = fade
#
#         # Delays inflation for a given amount of time
#         self.delay_inflation = delay_inflation
#
#     def run_sprite(self, screen, update_lock):
#         if not update_lock:
#             if self.delay_inflation == 0:
#                 self.update()
#             else:
#                 self.delay_inflation -= 1
#         self.draw(screen)
#
#     def update(self):
#         if self.current_scale[0] < self.stop_scale[0]:
#             self.current_scale[0] += self.scale_increment[0]
#             self.current_scale[1] += self.scale_increment[1]
#         if self.fade:
#             self.opacity -= self.fade_increment
#
#     def draw(self, screen):
#         new_surf = pygame.transform.scale(self.surface, [int(x) for x in self.current_scale]).convert_alpha()
#         rect = new_surf.get_rect()
#         rect.center = self.pos
#
#         if self.fade:
#             new_surf.fill((255, 255, 255, self.opacity if self.opacity >= 0 else 0), None, pygame.BLEND_RGBA_MULT)
#
#         screen.blit(new_surf, rect)
