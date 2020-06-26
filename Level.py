import pygame
import Constants
import Sprite
import time
import Button
import Globe
import copy

# GROUND LAYOUT
# T = Normal Tile
# W = Blank Spot
# B = Iron block

tile_dictionary = {'T': Constants.FLOOR_TILE_IMAGE, 'B': Constants.IRON_TILE_IMAGE, 'W': None, 'S': None}


class Level:
    def __init__(self, level_json):
        # Ground layout is a list of lists containing a grid of strings to draw the background of a level including
        # tiles like regular ground, and iron blocks
        self.ground_layout = None

        self.SPRITES = []
        self.delete_sprites = set([])

        # Since you shouldn't add sprites during iteration, they are queued to be added at the end of the loop
        self.sprite_queue = set([])

        '''
        # variables hold class instances for vortex tile, and any X tiles (xbox and xice are arrays of class instances
        # of X_Ice_Tile and X_Box_Tile classes)
        self.xice = set(xice)
        self.xbox = set(xbox)
        
        # list of boxes and explosions
        self.boxes = set(boxes)
        self.explosions = set([])
        # list of explosions to remove
        self.remove_explosions = set([])
        self.remove_boxes = set([])
        '''

        # Popups for pre and post level
        self.pre_level_popup_surf = None
        self.play_button = Button.Button(Constants.cscale(425, 440), Constants.cscale(180, 60),
                                         Constants.INLEVEL_PLAY_BUTTON_IMAGE, state_quantity=2)
        self.post_level_popup_surf = None
        self.next_level_button = Button.Button(Constants.cscale(55, 480), Constants.cscale(180, 60),
                                               Constants.NEXTLVL_BUTTON_IMAGE, state_quantity=2)

        # If true, game is paused
        self.update_lock = True
        # Prelevel and postlevel tracking variables
        self.start_level = False
        self.start_ending = False
        self.end_timer = 0

        # Name of the level
        self.name = None

        # If all X's have been satisfied, opens exit
        self.open_exit = False

        # Exit Button
        self.exit_button = Button.Button(Constants.cscale(550, 640), Constants.cscale(50, 50),
                                         Constants.EXIT_ICON_IMAGE, state_quantity=2)

        self.json = level_json
        self.load_level(level_json)

        # Time to beat the level.  Time_Runout used as a runonce variable to run a chunk of code when time runs out
        self.time_current = None
        self.time_diff = self.json["time"]
        self.time_runout = False
        # Saves response from time.time() and then calculates the difference to count down in the level
        self.start_time = 0

        # Set this to true when the level has been failed and needs a restart
        self.reset = False
        # Set this to true when the level has been beaten
        self.complete = False

        # Allows sprites to call a re-sort of the sprites
        self.sort_needed = False

        # Important pointers
        self.xice = []
        self.xbox = []
        self.boxes = []
        self.player = None
        self.vortex = None
        self.shadows = None

    def load_level(self, json):
        self.name = json["name"]
        self.ground_layout = json["layout"]
        # Adds player ball to sprites list
        self.add_sprite(Sprite.Player(None, 9, {"player"}, json["player_start"]))
        # Adds vortex to sprites list
        self.add_sprite(Sprite.Vortex(None, 8, {"vortex"}, json["vortex_pos"]))
        # Adds boxes
        for idx, box_pos in enumerate(self.json["box_poses"]):
            if self.json["box_types"][idx] == "ice":
                self.add_sprite(Sprite.IceCube(None, 10, {"box", "icecube"}, box_pos))
            else:
                self.add_sprite(Sprite.Box(None, 10, {"box"}, box_pos))
        # Adds X tiles
        for pos in json["ice_x_poses"]:
            self.add_sprite(Sprite.X_Ice_Tile(None, 1, {"xice"}, pos))
        for pos in json["box_x_poses"]:
            self.add_sprite(Sprite.X_Box_Tile(None, 1, {"xbox"}, pos))
        # Adds enemies
        for enemy in json["enemies"]:
            self.add_sprite(Sprite.Enemy(None, 9, "enemy", enemy["start_pos"], enemy["path_dir"], enemy["path_dist"]))
        # Adds image of ground layout to sprites
        ground_layout_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)

        # Draws the ground_layout
        grid_position = [0, 0]
        for row in self.ground_layout:
            for tile in row:
                if tile_dictionary[tile] is not None:
                    ground_layout_surf.blit(tile_dictionary[tile], grid_position)
                grid_position[0] += 50
            grid_position[1] += 50
            grid_position[0] = 0

        ground_layout_surf = pygame.transform.smoothscale(ground_layout_surf, Constants.cscale(1000, 600))
        self.add_sprite(Sprite.StaticImage(None, -1, {}, ground_layout_surf, (15, 15)))

        # Adds water
        self.add_sprite(Sprite.StaticImage(None, -2, {}, Constants.WATER_IMAGE, (15, 15)))

        # Adds shadows
        ground_layout_surf = pygame.Surface((1000, 600), pygame.SRCALPHA, 32)

        # Draws the ground_layout
        grid_position = [0, 0]
        for row in self.ground_layout:
            for tile in row:
                if tile == 'B' or tile == "S" or tile == "T":
                    ground_layout_surf.blit(Constants.WATER_SHADOW_IMAGE, grid_position)
                grid_position[0] += 50
            grid_position[1] += 50
            grid_position[0] = 0

        ground_layout_surf = pygame.transform.smoothscale(ground_layout_surf, Constants.cscale(1000, 600))
        self.add_sprite(Sprite.StaticImage(None, -10, {"shadows"}, ground_layout_surf, (15, 15)))

        self.add_new_sprites()

        # LOADS POPUPS FOR PRE AND POST LEVEL
        self.pre_level_popup_surf = pygame.Surface((430, 350))
        self.pre_level_popup_surf.fill((0, 0, 0))
        pygame.draw.rect(self.pre_level_popup_surf, (205, 175, 149), pygame.Rect(3, 3, 424, 344))

        rendered_text = Constants.get_arial(Constants.cscale(50, divisors=(1030,))).render('~*SILVERBALL*~', True, (0, 0, 0))
        self.pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 40)))

        rendered_text = Constants.get_arial(Constants.cscale(25, divisors=(1030,))).render('LEVEL:' + str(self.json["id"]), True, (0, 0, 0))
        self.pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 80)))

        rendered_text = Constants.get_arial(Constants.cscale(30, divisors=(1030,))).render('NAME', True, (0, 0, 0))
        self.pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 160)))

        rendered_text = Constants.get_arial(Constants.cscale(30, divisors=(1030,))).render('_____', True, (0, 0, 0))
        self.pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 165)))

        rendered_text = Constants.get_arial(Constants.cscale(35, divisors=(1030,))).render(self.json["name"], True, (0, 0, 0))
        self.pre_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(215, 210)))

        self.pre_level_popup_surf = pygame.transform.smoothscale(self.pre_level_popup_surf, Constants.cscale(430, 350))

        # POST LEVEL
        self.post_level_popup_surf = pygame.Surface((250, 450))
        self.post_level_popup_surf.fill((0, 0, 0))
        pygame.draw.rect(self.post_level_popup_surf, (205, 175, 149), pygame.Rect(3, 3, 244, 444))

        rendered_text = Constants.get_arial(Constants.cscale(40, divisors=(1030,))).render('LEVEL ' + str(self.json["id"]), True, (0, 0, 0))
        self.post_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(125, 40)))

        rendered_text = Constants.get_arial(Constants.cscale(40, divisors=(1030,))).render('COMPLETE!!', True, (0, 0, 0))
        self.post_level_popup_surf.blit(rendered_text, rendered_text.get_rect(center=(125, 80)))

        rendered_text = Constants.get_sans(Constants.cscale(38, divisors=(1030,))).render('SCORE:', True, (0, 0, 0))
        self.post_level_popup_surf.blit(rendered_text, (15, 160))

        rendered_text = Constants.get_sans(Constants.cscale(38, divisors=(1030,))).render('TOTAL SCORE:', True, (0, 0, 0))
        self.post_level_popup_surf.blit(rendered_text, (15, 270))

        self.post_level_popup_surf = pygame.transform.smoothscale(self.post_level_popup_surf, Constants.cscale(250, 450))

    def run_level(self, screen):
        # Draw Marble
        screen.blit(Constants.MARBLE_IMAGE, Constants.cscale(15, 15))

        if not self.update_lock and not self.start_ending:
            self.update()

        self.manage_sprites(screen)

        # Draws HotBar Items and Border
        #screen.blit(Constants.BORDER_IMAGE, (0, 0))

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(100, 640, 200, 58)), Constants.cscale(5))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(*Constants.cscale(300, 640, 200, 58)), Constants.cscale(5))

        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render('TIME: ' + str(self.time_diff), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(200, 669)))

        rendered_text = Constants.get_sans(Constants.cscale(50, divisors=(1030,))).render('LEVEL: ' + str(self.json["id"]), True, (0, 0, 0))
        screen.blit(rendered_text, rendered_text.get_rect(center=Constants.cscale(400, 669)))

        self.exit_button.draw(screen)
        self.exit_button.is_hover(pygame.mouse.get_pos())

        # Manage prelevel menu
        if not self.start_level:
            screen.blit(self.pre_level_popup_surf, self.pre_level_popup_surf.get_rect(center=(Constants.SCREEN_SIZE[0] / 2, Constants.SCREEN_SIZE[1] / 2)))

            self.play_button.draw(screen)
            self.play_button.is_hover(pygame.mouse.get_pos())
            for event in Globe.events:
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.play_button.is_clicked(event.pos):
                        self.start_level = True
                        self.update_lock = False
                        self.start_time = copy.copy(time.time())

        # Manage post menu level
        if self.start_ending:
            if self.end_timer < 50:
                self.end_timer += 1
            else:
                self.update_lock = True

                # Draws post-level menu
                screen.blit(self.post_level_popup_surf, self.post_level_popup_surf.get_rect(
                    center=Constants.cscale(160, 330)))

                score_gain = self.time_diff * 100 if not Globe.MENU.completed[self.json["id"] - 1] else 0

                rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(score_gain), True, (0, 0, 0))
                self.post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 190))

                rendered_text = Constants.get_sans(Constants.cscale(36, divisors=(1030,))).render(str(Globe.MENU.score + score_gain), True, (0, 0, 0))
                self.post_level_popup_surf.blit(rendered_text, Constants.cscale(15, 300))

                self.next_level_button.draw(screen)
                self.next_level_button.is_hover(pygame.mouse.get_pos())
                for event in Globe.events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.next_level_button.is_clicked(event.pos):
                            self.complete = True

        if self.sort_needed:
            self.sort_needed = False
            self.sort_sprites()

    def event_handler(self):
        for event in Globe.events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.exit_button.is_clicked(event.pos):
                    Globe.MENU.menu_state = 'main'

    def add_sprite(self, sprite):
        self.sprite_queue.add(sprite)

    def manage_sprites(self, screen):
        # Runs sprites
        for sprite in self.SPRITES:
            sprite.run_sprite(screen, self.update_lock)

            # Deletes killed sprites
            if sprite.kill:
                self.delete_sprites.add(sprite)
            # Manages lifetime
            if sprite.lifetime is not None and not self.update_lock:
                if sprite.lifetime <= 0:
                    self.delete_sprites.add(sprite)
                sprite.lifetime -= 1

        # Removes dead sprites
        for sprite in self.delete_sprites:
            if sprite in self.SPRITES:
                self.SPRITES.remove(sprite)

        self.add_new_sprites()

    def add_new_sprites(self):
        # Add new sprites
        for sprite in self.sprite_queue:
            self.SPRITES.append(sprite)
        if len(self.sprite_queue):
            self.sort_sprites()
            self.sprite_queue = set([])

    def sort_sprites(self):
        self.SPRITES = sorted(self.SPRITES, key=lambda spr: spr.z_order)

    def update(self):
        self.xice = [sprite for sprite in self.SPRITES if "xice" in sprite.tags]
        self.xbox = [sprite for sprite in self.SPRITES if "xbox" in sprite.tags]
        self.boxes = [sprite for sprite in self.SPRITES if "box" in sprite.tags]
        self.vortex = [sprite for sprite in self.SPRITES if "vortex" in sprite.tags][0]
        self.player = [sprite for sprite in self.SPRITES if "player" in sprite.tags][0]
        self.shadows = [sprite for sprite in self.SPRITES if "shadows" in sprite.tags][0]

        self.event_handler()

        # Detects if all X marks are satisfied. open_exit initially set to false
        self.open_exit = False
        # temporary array to report the status of each x mark
        x_satisfaction = True
        # If there are no Xs, exit opens automatically
        if not len(self.xice) and not len(self.xbox):
            self.open_exit = True
        else:
            # Checks if any X's aren't satisfied
            for x in self.xice:
                satisfied = False
                for box in self.boxes:
                    if "icecube" in box.tags and box.coords == x.coords:
                        satisfied = True
                if not satisfied:
                    x_satisfaction = False

            for x in self.xbox:
                satisfied = False
                for box in self.boxes:
                    if box.coords == x.coords:
                        satisfied = True
                if not satisfied:
                    x_satisfaction = False

            # If all Xs are satisfied, exit opens
            if x_satisfaction:
                self.open_exit = True

        # controls animations with vortex
        if self.open_exit and self.vortex.state == 'blank':
            self.vortex.set_image = False
            self.vortex.state = 'open'
        elif not self.open_exit and self.vortex.state == 'stationary':
            self.vortex.set_image = False
            self.vortex.state = 'close'

        # Counts timer and resets game if time runs out
        self.time_current = time.time()
        self.time_diff = self.json["time"] - int(self.time_current - self.start_time)

        if self.time_diff <= 0:
            self.player.set_drown()
            if not self.reset:
                Globe.MENU.GAME.add_sprite(Sprite.Animation(-1, 5, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
                                           Constants.cscale(*self.player.pos), 74))
            self.reset = True
