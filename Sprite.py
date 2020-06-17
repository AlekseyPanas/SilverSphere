class Player:
    def __init__(self, coords, image, image_up, image_down, image_right, image_left):
        # position and grid coords
        self.coords = coords
        self.pos = [(self.coords[0] * 50) + 40, (self.coords[1] * 50) + 40]

        # Images for stationary and movement animations
        self.image = image
        self.img_l = image_left
        self.img_r = image_right
        self.img_u = image_up
        self.img_d = image_down

        # Image and Animation info
        self.time = 4
        self.image_center = [130, 130]
        self.image_size = [260, 260]
        self.desired_image_size = [51, 51]
        # When moving, changes current image to the animation image for the corresponding direction of movement
        self.current_image = image

        # state
        self.state = "Stationary"
        # list holding info on whether or not there are boxes in either of the 4 directions of the cube
        self.near_boxes = [None, None, None, None]

        # used to track movement
        self.count = 0

        # Run-Once variable for setting box state
        self.set_box_state = False

    def draw(self, c):
        # Continuously calls Update
        self.update()

        # Draws Ball Shadow
        c.draw_image(ball_shadow, [260, 260], [520, 520], [self.pos[0] + 25, self.pos[1] + 25], [100, 100])

        # When stationary
        if self.state == "Stationary" or self.state == 'drown':
            c.draw_image(self.image, [130, 130], [260, 260], self.pos, [50, 50])
        # moving animation
        if self.state == "Right" or self.state == "Left" or self.state == "Up" or self.state == "Down":
            self.animate(c)

    def update(self):
        # Update Coords
        self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
        # if not moving, detects button presses. When button pressed down, set animation image and set corresponding
        # state Calls predetect to see if you are allowed to move in a certain direction (nothing blocking like iron
        # boxes or the map border... etc)
        if self.state == "Stationary":
            if STACK.peek() == 'r' and self.pre_detect()[0] == True:
                self.state = "Right"
                self.current_image = self.img_r
            elif STACK.peek() == 'l' and self.pre_detect()[1] == True:
                self.state = "Left"
                self.current_image = self.img_l
            elif STACK.peek() == 'u' and self.pre_detect()[2] == True:
                self.state = "Up"
                self.current_image = self.img_u
            elif STACK.peek() == 'd' and self.pre_detect()[3] == True:
                self.state = "Down"
                self.current_image = self.img_d
        # Moving function called continuously
        self.move()

    def move(self):
        # If any directional state is the current state, then run the code
        if self.state == "Right" or self.state == "Left" or self.state == "Up" or self.state == "Down":
            # Moves ball continuously in direction corresponding to the state
            # If there is a box in the direction you are moving, set the state of the box to move in the corresponding
            # direction. The set_box_state is a
            # run once variable to make the state be set only once until you move again.
            if self.state == "Right":
                if self.set_box_state == False and not self.near_boxes[0] == None:
                    self.set_box_state = True
                    self.near_boxes[0].state = 'Right'
                self.pos[0] += 5
            elif self.state == "Left":
                if self.set_box_state == False and not self.near_boxes[1] == None:
                    self.set_box_state = True
                    self.near_boxes[1].state = 'Left'
                self.pos[0] -= 5
            elif self.state == "Up":
                if self.set_box_state == False and not self.near_boxes[2] == None:
                    self.set_box_state = True
                    self.near_boxes[2].state = 'Up'
                self.pos[1] -= 5
            elif self.state == "Down":
                if self.set_box_state == False and not self.near_boxes[3] == None:
                    self.set_box_state = True
                    self.near_boxes[3].state = 'Down'
                self.pos[1] += 5
            # Increment count
            self.count += 5
            # Detects when the ball has moved a single tile and then sets state to Stationary. Also resets count
            if self.count >= 50:
                self.state = "Stationary"
                self.count = 0
                # Updates Coords and runs post-detect
                self.coords = [(self.pos[0] - 40) / 50, (self.pos[1] - 40) / 50]
                self.post_detect()

    def pre_detect(self):
        self.allowed_movement = [True, True, True, True]
        self.near_boxes = [None, None, None, None]
        self.set_box_state = False
        # Detects if the end of the map is in any direction of the player
        if self.coords[0] == 19:
            self.allowed_movement[0] = False
        if self.coords[0] == 0:
            self.allowed_movement[1] = False
        if self.coords[1] == 11:
            self.allowed_movement[3] = False
        if self.coords[1] == 0:
            self.allowed_movement[2] = False

        # Detects metal boxes
        if self.allowed_movement[0] == True and GLOBAL.CURRENT_LVL.ground_layout[int(self.coords[1])][
            int(self.coords[0]) + 1] == 'B':
            self.allowed_movement[0] = False
        if self.allowed_movement[1] == True and GLOBAL.CURRENT_LVL.ground_layout[int(self.coords[1])][
            int(self.coords[0]) - 1] == 'B':
            self.allowed_movement[1] = False
        if self.allowed_movement[2] == True and GLOBAL.CURRENT_LVL.ground_layout[int(self.coords[1]) - 1][
            int(self.coords[0])] == 'B':
            self.allowed_movement[2] = False
        if self.allowed_movement[3] == True and GLOBAL.CURRENT_LVL.ground_layout[int(self.coords[1]) + 1][
            int(self.coords[0])] == 'B':
            self.allowed_movement[3] = False

        # Detects boxes that aren't in the water
        # If the box is not able to be pushed in a certain direction (box.detect() returns that info) then allowed movement is set to false for that direction
        for box in GLOBAL.CURRENT_LVL.boxes:
            if not box.state == 'drown':
                if self.allowed_movement[0] == True and box.coords == [self.coords[0] + 1, self.coords[1]]:
                    self.near_boxes[0] = box
                    if box.detect()[0] == False:
                        self.allowed_movement[0] = False
                if self.allowed_movement[1] == True and box.coords == [self.coords[0] - 1, self.coords[1]]:
                    self.near_boxes[1] = box
                    if box.detect()[1] == False:
                        self.allowed_movement[1] = False
                if self.allowed_movement[2] == True and box.coords == [self.coords[0], self.coords[1] - 1]:
                    self.near_boxes[2] = box
                    if box.detect()[2] == False:
                        self.allowed_movement[2] = False
                if self.allowed_movement[3] == True and box.coords == [self.coords[0], self.coords[1] + 1]:
                    self.near_boxes[3] = box
                    if box.detect()[3] == False:
                        self.allowed_movement[3] = False

        # Returns an array which says whether or not movement in a certain direction is allowed
        # [Right,Left,Up,Down]
        return self.allowed_movement

    def post_detect(self):
        # detects if player is standing on water and sets state to drown as well as starts reset timer if on water
        if GLOBAL.CURRENT_LVL.ground_layout[int(self.coords[1])][int(self.coords[0])] == 'W':
            self.state = 'drown'
            reset_timer.start()

        # Detects if on vortex
        elif GLOBAL.CURRENT_LVL.vortex.coords == self.coords and GLOBAL.CURRENT_LVL.vortex.state == 'stationary':
            # sets the vortex to close
            GLOBAL.CURRENT_LVL.vortex.set_image = False
            GLOBAL.CURRENT_LVL.vortex.state = 'close'
            # State drown to make player disappear under the tiles
            self.state = 'drown'
            # starts timer to open post level menu
            post_timer.start()

    def animate(self, canvas):
        self.current_index = (self.time % 24) // 6
        self.current_center = [self.image_center[0] + self.current_index * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.current_image, self.current_center, self.image_size, self.pos, self.desired_image_size)
        self.time += 0.95
