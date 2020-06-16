import Level
import pygame

# Stores all global variables
class global_store:
    def __init__(self,menu):
        # Array of levels
        self.levels = []
        # list of booleans corresponding to whether the level in the same index as above has been completed
        self.completed = []

        # Level thats currently selected
        self.CURRENT_LVL = None
        self.CURRENT_LVL_IDX = None

        # What state is the game in
        self.gamestate = 'Menu'

        # Instantiates menu class
        self.MENU = menu

        # variable to store game score
        self.score = 0
        # score earned from the level that you just beat
        self.current_score = 0

        # Images!
        # IMAGE LOADING AND SIZE TRANSFORMATION
        self.menu_sky = pygame.image.load("assets/images/cloud.png").convert_alpha()
        self.menu_image = pygame.image.load('assets/images/title screen.png').convert_alpha()

        self.marble_image = pygame.image.load("assets/images/marble background.png")

        # Button images
        self.play_button_image = pygame.image.load("assets/images/title play.png")
        self.inlevel_play_button_image = pygame.image.load("assets/images/play.png")
        self.next_level_button_image = pygame.image.load("assets/images/nxtlvl.png")
        self.levelsel_button_image = pygame.image.load("assets/images/level select button.png")
        self.exit_icon = pygame.image.load("assets/images/X.png")

    def define_levels(self):
        #######ADD LEVELS HERE########
        self.levels = []

        # What the Level class takes as parameters
        # ground_layout, player_start_pos, vortex, boxes, name, time, xbox = [], xice = []

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],  # 3
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 4
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 5
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T'],  # 6
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T'],  # 7
             ['T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 8
             ['T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 9
             ['T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 10
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 1], Vortex([17, 4]), [Box([7, 2]), Box([6, 2])], 'ORIGIN', 30, self))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['T', 'T', 'T', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 4
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 5
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 6
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 7
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 8
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 9
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 10
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 1], Vortex([11, 4]), [Box([2, 3]), Box([2, 6]), Box([2, 9])], 'FORTRESS', 45, self))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 4
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 5
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W', 'B', 'B', 'B', 'B', 'B', 'W', 'W', 'W', 'W', 'W', 'W'],  # 6
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 7
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 8
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 9
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 10
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 2], Vortex([11, 4]), [IceCube([2, 3]), Box([6, 3]), Box([4, 0]), Box([10, 4])], 'ALOTA X', 110, self,
            [X_Box_Tile([0, 11]), X_Box_Tile([5, 0])], [X_Ice_Tile([1, 11])]))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'W', 'W', 'W', 'T', 'T', 'W', 'W', 'W', 'W', 'T', 'T', 'W', 'W', 'T', 'T', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W'],  # 2
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W'],  # 3
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W'],  # 4
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 5
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T'],  # 6
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'T', 'T'],  # 7
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T'],  # 8
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T'],  # 9
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T'],  # 10
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 1], Vortex([18, 9]), [IceCube([4, 4]), Box([2, 4]), Box([6, 2]), Box([1, 10])], 'TRAVERSE', 90, self,
            [], [X_Ice_Tile([17, 3])]))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'T', 'W', 'W', 'T', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['W', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['W', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 4
             ['W', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W'],  # 5
             ['W', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'T', 'W', 'W', 'W', 'W'],  # 6
             ['W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'T', 'W', 'W', 'W', 'T', 'W', 'W', 'T', 'T', 'T', 'T', 'W'],  # 7
             ['W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'T', 'W'],  # 8
             ['W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 9
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 10
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T']],
            # 11
            [1, 1], Vortex([18, 10]), [Box([12, 5])], 'ACTIVE', 30, self,
            [X_Box_Tile([5, 8])]))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'B', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'W', 'W', 'W', 'T', 'T', 'T', 'B', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 4
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'B', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 5
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'B', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 6
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'B', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 7
             ['W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 8
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 9
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 10
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 1], Vortex([12, 1]), [Box([7, 1]), Box([12, 1]), Box([7, 8]), Box([7, 7]), Box([7, 6])], 'ISLANDER', 45, self,
            [X_Box_Tile([12, 7])]))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'W', 'T', 'W', 'T', 'T'],  # 2
             ['W', 'T', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'B'],  # 3
             ['W', 'T', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'W', 'T', 'W', 'T', 'T'],  # 4
             ['W', 'T', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'T'],  # 5
             ['W', 'T', 'T', 'W', 'T', 'T', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'T'],  # 6
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 7
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 8
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 9
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 10
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']],
            # 11
            [1, 1], Vortex([17, 8]), [Box([16, 3]), Box([10, 3]), Box([8, 3])], 'OBSTACLE', 30))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 4
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 5
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 6
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 7
             ['W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 8
             ['W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'T', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 9
             ['T', 'T', 'T', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 10
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T']],
            # 11
            [1, 1], Vortex([18, 10]), [IceCube([1, 6]), Box([11, 1]), Box([11, 6])], 'GUIDANCE', 45, self,
            [], [X_Ice_Tile([6, 1])]))

        #						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level.Level(
            [['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 0
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 1
             ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 2
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],  # 3
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 4
             ['W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 5
             ['W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'T'],  # 6
             ['W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'T'],  # 7
             ['W', 'W', 'T', 'T', 'T', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 8
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 9
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T'],  # 10
             ['W', 'W', 'W', 'W', 'W', 'T', 'T', 'T', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'T', 'T', 'T']],
            # 11
            [1, 1], Vortex([18, 10]), [IceCube([6, 1]), Box([3, 6])], 'PATHWAY', 45, self,
            [], [X_Ice_Tile([18, 6])]))

        '''#						    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
        self.levels.append(Level([['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #0
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #1
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #2
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #3
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #4
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #5
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #6
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #7
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #8
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #9
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W'],  #10
                                  ['W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W','W']], #11
                                  [],Vortex([]),[IceCube([]),Box([])],'',10,
                                  [X_Box_Tile([])],[X_Ice_Tile([])]))'''