import Button

class Level:
    def __init__(self, ground_layout, player_start_pos, vortex, boxes, name, time, global_class_reference, xbox=[], xice=[]):
        # A reference to the class will be passed so it can be used
        self.GLOBAL = global_class_reference

        # Ground layout is a list of lists containing a grid of strings to draw the background of a level including tiles like
        # regular ground, and iron blocks
        self.ground_layout = ground_layout
        # variables hold class instances for vortex tile, and any X tiles (xbox and xice are arrays of class instances of X_Ice_Tile and X_Box_Tile classes)
        self.vortex = vortex
        self.xice = set(xice)
        self.xbox = set(xbox)

        # Player class instance
        self.PLYR = Player(player_start_pos, player, player_up, player_down, player_right, player_left)

        # list of boxes and explosions
        self.boxes = set(boxes)
        self.explosions = set([])
        # list of explosions to remove
        self.remove_explosions = set([])
        self.remove_boxes = set([])

        # Name of the level
        self.name = name

        # If all X's have been satisfied, opens exit
        self.open_exit = False

        # Time to beat the level.  Time_Runout used as a runonce variable to run a chunk of code when time runs out
        self.time = time
        self.time_runout = 0
        self.second = 0

        # Exit Button
        self.exit_button = Button.Button([0, 0], self.GLOBAL.exit_icon, [50, 50])

    def mouse(self, pos):
        if self.exit_button.click(pos):
            self.GLOBAL.MENU.menustate = 'main'
            self.GLOBAL.gamestate = 'Menu'

    def draw_level(self, canvas):
        # Variable used to track current position on grid when drawing level
        self.grid_position = [40, 40]

        # Draw Marble
        canvas.draw_image(self.GLOBAL.marble_image, [515, 350], [1030, 700], [515, 350], [1030, 700])

        # Draws water shadows
        for row in self.ground_layout:
            for tile in row:
                if tile == 'T' or tile == 'B' or tile == 'S':
                    canvas.draw_image(water_shadow, [260, 260], [520, 520],
                                      [self.grid_position[0] + 25, self.grid_position[1] + 25], [100, 100])
                self.grid_position[0] += 50
            self.grid_position[1] += 50
            self.grid_position[0] = 40

            # Draws player before tiles (When sunken to create underwater effect)
        if self.PLYR.state == 'drown':
            self.PLYR.draw(canvas)

            # Draw Boxes before tiles for sink effect
        for box in self.boxes:
            if box.state == 'drown':
                box.draw(canvas)

        # Draw Water
        canvas.draw_image(water_image, [515, 350], [1030, 700], [515, 350], [1030, 700])

        # Reset Grid Position
        self.grid_position = [40, 40]

        # Draws the ground_layout
        for row in self.ground_layout:
            for tile in row:
                canvas.draw_image(tile_dictionary[tile], [130, 130], [260, 260], self.grid_position, [50, 50])
                self.grid_position[0] += 50
            self.grid_position[1] += 50
            self.grid_position[0] = 40

        # Detects if all X marks are satisfied. open_exit initially set to false
        self.open_exit = False
        # temporary array to report the status of each x mark
        self.x_satisfaction = []
        # Temporary variable to tell if TRUE has already been added to the list
        self.status_added = False
        # If there are no Xs, exit opens automatically
        if len(self.xice) == 0 and len(self.xbox) == 0:
            self.open_exit = True
        else:
            # Adds the state of each X to the satisfaction list
            for x in self.xice:
                for box in self.boxes:
                    if box.__name__ == 'IceCube' and box.coords == x.coords:
                        self.x_satisfaction.append(True)
                        self.status_added = True
                if self.status_added == False:
                    self.x_satisfaction.append(False)
                self.status_added = False

            # status added set to false
            self.status_added = False

            for x in self.xbox:
                for box in self.boxes:
                    if box.__name__ == 'Box' and box.coords == x.coords:
                        self.x_satisfaction.append(True)
                        self.status_added = True
                if self.status_added == False:
                    self.x_satisfaction.append(False)
                self.status_added = False

            # If all Xs are satisfied, exit opens
            # print(self.x_satisfaction)
            # print(False in self.x_satisfaction)
            # print(not (False in self.x_satisfaction))
            if not (False in self.x_satisfaction):
                self.open_exit = True

                # controls animations with vortex
        if self.open_exit == True and self.vortex.state == 'blank':
            self.vortex.set_image = False
            self.vortex.state = 'open'
        elif self.open_exit == False and self.vortex.state == 'stationary':
            self.vortex.set_image = False
            self.vortex.state = 'close'

        # Draws the vortex and any X tiles
        self.vortex.draw(canvas)
        for tile in self.xice:
            tile.draw(canvas)
        for tile in self.xbox:
            tile.draw(canvas)

        # Draws Player After Tiles
        if not self.PLYR.state == 'drown':
            self.PLYR.draw(canvas)

        # Draws boxes
        for box in self.boxes:
            if not box.state == 'drown':
                box.draw(canvas)

        # Draws explosions and adds explosions to be removed that exceeded their lifespan
        for expl in self.explosions:
            expl.animate(canvas)
            if expl.lifetime >= 64:
                self.remove_explosions.add(expl)

        # Draws HotBar Items and Border
        canvas.draw_image(border_image, [515, 350], [1030, 700], [515, 350], [1030, 700])
        canvas.draw_polygon([[100, 640], [300, 640], [300, 698], [100, 698]], 5, 'Black')
        canvas.draw_text('TIME: ' + str(self.time), [115, 680], 40, 'Black')
        canvas.draw_polygon([[300, 640], [500, 640], [500, 698], [300, 698]], 5, 'Black')
        canvas.draw_text('LEVEL ' + str(GLOBAL.CURRENT_LVL_IDX + 1), [315, 680], 40, 'Black')
        self.exit_button.center = [550, 665]
        self.exit_button.draw(canvas)

        # removes explosions and boxes that need removing. Cleares explosion list in between
        for expl in self.remove_explosions:
            if expl in self.explosions:
                self.explosions.remove(expl)

        self.remove_explosions = set([])

        for box in self.remove_boxes:
            if box in self.boxes:
                self.explosions.add(Explode(box.pos))
                self.boxes.remove(box)

        # Timer when this function has been called 60 times, a second has passed so time is decremented
        if self.second >= 60:
            self.second = 0
            self.time -= 1

        # If the time goes to 0 or under, player is set to drown and then the reset timer starts to reset the level
        # An explosion is appended to the list to play the explosion animation at players position
        if self.time <= 0 and self.time_runout == 0:
            self.PLYR.state = 'drown'
            reset_timer.start()
            self.time_runout = 1
            self.explosions.add(Explode(self.PLYR.pos))

        self.second += 1