import pygame
import Constants
from sprites.Sprite import Sprite
import time
import Button
import copy





# GROUND LAYOUT
# T = Normal Tile
# W = Blank Spot
# B = Iron block




class Level:
    def __init__(self, level_json: dict):


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

        # Ground layout is a list of lists containing a grid of strings to draw the background of a level including
        # tiles like regular ground, and iron blocks
        self.ground_layout: list[list[str]] | None = None

        self.SPRITES = []
        self.delete_sprites = set([])

        # Since you shouldn't add sprites during iteration, they are queued to be added at the end of the loop
        self.sprite_queue = set([])

        # Popups for pre- and post-level
        self.pre_level_popup_surf = None
        self.play_button = Button.Button(Constants.cscale(425, 440), Constants.cscale(180, 60),
                                         self.INLEVEL_PLAY_BUTTON_IMAGE, state_quantity=2)
        self.post_level_popup_surf = None
        self.next_level_button = Button.Button(Constants.cscale(55, 480), Constants.cscale(180, 60),
                                               self.NEXTLVL_BUTTON_IMAGE, state_quantity=2)

        # If true, game is paused
        self.update_lock = True
        # Prelevel and postlevel tracking variables
        self.start_level = False
        self.start_ending = False
        self.end_timer = 0

        # Name of the level
        self.name: str | None = None

        # If all X's have been satisfied, opens exit
        self.open_exit = False

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


        if not self.update_lock and not self.start_ending:
            self.update()

        self.manage_sprites(screen)

        # Draws HotBar Items and Border
        #screen.blit(Constants.BORDER_IMAGE, (0, 0))



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

    def update(self):

        # Counts timer and resets game if time runs out
        self.time_current = time.time()
        self.time_diff = self.json["time"] - int(self.time_current - self.start_time)

        if self.time_diff <= 0:
            self.player.set_drown()
            if not self.reset:
                Globe.MENU.game.add_sprite(Sprite.Animation(-1, 5, {}, (9, 9), 1, Constants.EXPLOSION_IMAGE,
                                                            Constants.cscale(*self.player.pos), 74))
            self.reset = True
