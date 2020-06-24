import pygame
import Constants
import Globe


class Object:
    def __init__(self, lifetime, z_order, tags):
        self.lifetime = lifetime
        self.kill = False

        # Draw order
        self.z_order = z_order

        # Set of string tags that can identify an object
        self.tags = set(tags)

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
        return (coords[0] * 50) + 40, (coords[1] * 50) + 40

    def run_sprite(self, screen, update_lock):
        pass


class StaticImage(Object):
    def __init__(self, lifetime, z_order, tags, image, pos):
        super().__init__(lifetime, z_order, tags)

        self.image = image
        self.pos = pos

    def run_sprite(self, screen, update_lock):
        screen.blit(self.image, Constants.cscale(*self.pos))


class Player(Object):
    def __init__(self, lifetime, z_order, tags, coords):
        super().__init__(lifetime, z_order, tags)

        # position and grid coords
        self.coords = coords
        self.pos = list(Object.get_center_from_coords(self.coords))

        # Key press stack for controlling ball
        self.STACK = Constants.Stack()

        # Images for stationary and movement animations
        self.image = Constants.PLAYER_IMAGE
        self.img_l = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
        self.img_r = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
        self.img_u = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]
        self.img_d = [pygame.Surface(Constants.cscale(51, 51), pygame.SRCALPHA, 32) for x in range(4)]

        # Blits each frame onto the respective surface of the list of animation surfaces
        [self.img_l[i].blit(Constants.PLAYER_LEFT_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_l))]
        [self.img_r[i].blit(Constants.PLAYER_RIGHT_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_r))]
        [self.img_u[i].blit(Constants.PLAYER_UP_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_u))]
        [self.img_d[i].blit(Constants.PLAYER_DOWN_IMAGE, (-i * Constants.cscale(51), 0)) for i in range(len(self.img_d))]

        # Image and Animation info
        self.time = 0
        # When moving, changes current image to the animation image for the corresponding direction of movement
        self.current_image = self.image

        # state
        self.state = "static"
        # list holding info on whether or not there are boxes in either of the 4 directions of the cube
        self.near_boxes = [None for x in range(4)]

        # used to track movement
        self.move_count = 0

        # Run-Once variable for setting box state
        self.set_box_state = False

    def run_sprite(self, screen, update_lock):
        if not update_lock:
            self.update()
        self.draw(screen, update_lock)

    def draw(self, screen, update_lock):
        # Draws Ball Shadow
        screen.blit(Constants.BALL_SHADOW_IMAGE,
                    Constants.BALL_SHADOW_IMAGE.get_rect(center=Constants.cscale(self.pos[0] + 10, self.pos[1] + 22)))

        # Draws ball
        # When stationary
        if self.state == "static" or self.state == 'drown':
            screen.blit(self.image, self.image.get_rect(center=Constants.cscale(*self.pos)))
        # moving animation
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            self.animate(screen, update_lock)

    def animate(self, screen, update_lock):
        current_index = int((self.time % 24) // 6)
        screen.blit(self.current_image[current_index], self.image.get_rect(center=Constants.cscale(*self.pos)))
        if not update_lock:
            self.time += 0.95

    def event_handler(self):
        for event in Globe.events:
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

    def update(self):
        # Calls event handler
        self.event_handler()

        # Update coordinate location on game grid
        self.coords = ((self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50)
        # if not moving, detects button presses. When button pressed down, set animation image and set corresponding
        # state. Calls pre-detect to see if you are allowed to move in a certain direction (nothing blocking like iron
        # boxes or the map border... etc)
        if self.state == "static":
            detect = self.pre_detect()
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
        self.move()

    def move(self):
        # If any directional state is the current state, then run the code
        if self.state == "r" or self.state == "l" or self.state == "u" or self.state == "d":
            # Moves ball continuously in direction corresponding to the state
            # If there is a box in the direction you are moving, set the state of the box to move in the corresponding
            # direction. The set_box_state is a
            # run once variable to make the state be set only once until you move again.
            if self.state == "r":
                if not self.set_box_state and not self.near_boxes[0] is None:
                    self.set_box_state = True
                    self.near_boxes[0].state = 'r'
                self.pos[0] += 5
            elif self.state == "l":
                if not self.set_box_state and not self.near_boxes[1] is None:
                    self.set_box_state = True
                    self.near_boxes[1].state = 'l'
                self.pos[0] -= 5
            elif self.state == "u":
                if not self.set_box_state and not self.near_boxes[2] is None:
                    self.set_box_state = True
                    self.near_boxes[2].state = 'u'
                self.pos[1] -= 5
            elif self.state == "d":
                if not self.set_box_state and not self.near_boxes[3] is None:
                    self.set_box_state = True
                    self.near_boxes[3].state = 'd'
                self.pos[1] += 5
            # Increment count
            self.move_count += 5
            # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
            if self.move_count >= 50:
                self.state = "static"
                self.move_count = 0
                # Updates Coords and runs post-detect
                self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
                self.post_detect()

    def pre_detect(self):
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
        if allowed_movement[0] and Globe.MENU.GAME.ground_layout[int(self.coords[1])][int(self.coords[0]) + 1] == 'B':
            allowed_movement[0] = False
        if allowed_movement[1] and Globe.MENU.GAME.ground_layout[int(self.coords[1])][int(self.coords[0]) - 1] == 'B':
            allowed_movement[1] = False
        if allowed_movement[2] and Globe.MENU.GAME.ground_layout[int(self.coords[1]) - 1][int(self.coords[0])] == 'B':
            allowed_movement[2] = False
        if allowed_movement[3] and Globe.MENU.GAME.ground_layout[int(self.coords[1]) + 1][int(self.coords[0])] == 'B':
            allowed_movement[3] = False

        # Detects boxes that aren't in the water
        # If the box is not able to be pushed in a certain direction
        # (box.detect() returns that info) then allowed movement is set to false for that direction
        for box in [sprite for sprite in Globe.MENU.GAME.SPRITES if "box" in sprite.tags]:
            if not box.state == 'drown':
                box_detect = box.detect()
                if allowed_movement[0] and box.coords == [self.coords[0] + 1, self.coords[1]]:
                    self.near_boxes[0] = box
                    if not box_detect[0]:
                        allowed_movement[0] = False
                if allowed_movement[1] and box.coords == [self.coords[0] - 1, self.coords[1]]:
                    self.near_boxes[1] = box
                    if not box_detect[1]:
                        allowed_movement[1] = False
                if allowed_movement[2] and box.coords == [self.coords[0], self.coords[1] - 1]:
                    self.near_boxes[2] = box
                    if not box_detect[2]:
                        allowed_movement[2] = False
                if allowed_movement[3] and box.coords == [self.coords[0], self.coords[1] + 1]:
                    self.near_boxes[3] = box
                    if not box_detect[3]:
                        allowed_movement[3] = False

        # Returns an array which says whether or not movement in a certain direction is allowed
        # [Right,Left,Up,Down]
        return allowed_movement

    def post_detect(self):
        vortex = [sprite for sprite in Globe.MENU.GAME.SPRITES if "vortex" in sprite.tags][0]

        # detects if player is standing on water and sets state to drown as well as starts reset timer if on water
        if Globe.MENU.GAME.ground_layout[int(self.coords[1])][int(self.coords[0])] == 'W':
            self.state = 'drown'
            Globe.MENU.GAME.reset = True

            self.z_order = -3
            Globe.MENU.GAME.sort_needed = True

        # Detects if on vortex
        elif vortex.coords == self.coords and vortex.state == 'stationary':
            # sets the vortex to close
            vortex.set_image = False
            vortex.state = 'close'
            # State drown to make player disappear under the tiles
            self.state = 'drown'
            # starts timer to open post level menu
            Globe.MENU.GAME.start_ending = True

            self.z_order = -3
            Globe.MENU.GAME.sort_needed = True


class Vortex(Object):
    def __init__(self, lifetime, z_order, tags, coords):
        super().__init__(lifetime, z_order, tags)
        self.coords = coords
        self.pos = Object.get_center_from_coords(coords)
        self.state = 'blank'
        # Vortex animation images
        self.open = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(9)]
        self.close = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(9)]
        self.stationary = [pygame.Surface(Constants.cscale(70, 70), pygame.SRCALPHA, 32) for x in range(11)]

        # Blits each frame onto the respective surface of the list of animation surfaces
        [self.open[i].blit(Constants.VORTEX_OPEN_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.open))]
        [self.close[i].blit(Constants.VORTEX_CLOSE_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.close))]
        [self.stationary[i].blit(Constants.VORTEX_TILE_IMAGE, (-i * Constants.cscale(70), 0)) for i in range(len(self.stationary))]

        self.current_image = None
        # run once variable to set image
        self.set_image = False

        # animation variables   frames, and animation speed
        self.time = 0
        self.frames = 1
        self.animation_speed = 0.21

    def run_sprite(self, screen, update_lock):
        if not update_lock:
            self.update()
        self.draw(screen, update_lock)

    def update(self):
        if self.state == 'open' or self.state == 'close':
            # sets image, frames, and animation speed, resets time to start animation from the beginning
            if not self.set_image and self.state == 'close':
                self.current_image = self.close
                self.set_image = True
                self.frames = 9
                self.animation_speed = 0.21
                self.time = 0
            elif not self.set_image and self.state == 'open':
                self.current_image = self.open
                self.set_image = True
                self.frames = 9
                self.animation_speed = 0.21
                self.time = 0

        elif self.state == 'stationary':
            if not self.set_image:
                self.current_image = self.stationary
                self.set_image = True
                self.frames = 11
                self.animation_speed = 0.28
                self.time = 0

            # FIX THIS: Checks for boxes on open vortex and sets them to explode
            '''for box in GLOBAL.CURRENT_LVL.boxes:
                if box.coords == self.coords:
                    GLOBAL.CURRENT_LVL.remove_boxes.add(box)'''

        else:
            self.current_image = None

    def draw(self, screen, update_lock):
        if not self.state == 'blank':
            # increment duration and animate image
            self.animate(screen, update_lock)

    def animate(self, screen, update_lock):
        current_index = int(self.time % self.frames)
        if self.current_image is not None:
            screen.blit(self.current_image[current_index], self.current_image[0].get_rect(center=Constants.cscale(*self.pos)))
        if not update_lock:
            self.time += self.animation_speed
            # Checks if animation ended
            if self.state == 'open' or self.state == 'close':
                if self.time > 1 and int(self.time % self.frames) == 0:
                    if self.state == 'open':
                        self.state = 'stationary'
                    elif self.state == 'close':
                        self.state = 'blank'
                    self.set_image = False
