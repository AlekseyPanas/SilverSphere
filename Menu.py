import Constants
import json
import pygame
from enum import IntEnum
from typing import Optional
from managers.Managers import Manager, ASSET_LOADER
from managers.BirthdayManager import BirthdayManager
from managers.MenuScreenMainManager import MenuScreenMainManager
from managers.MenuScreenLevelSelectManager import MenuScreenLevelSelectManager
from managers.GameManager import GameManager
import inspect


class MenuStates(IntEnum):
    MAIN = 0
    LEVELSEL = 1
    CUSTOMLEVELSEL = 2
    BIRTHDAY = 3
    GAME = 4


STATE_TO_CLASS = {MenuStates.MAIN: MenuScreenMainManager,
                  MenuStates.LEVELSEL: MenuScreenLevelSelectManager,
                  MenuStates.CUSTOMLEVELSEL: Manager,
                  MenuStates.BIRTHDAY: BirthdayManager,
                  MenuStates.GAME: GameManager}


class Menu:
    """
    Primary app manager class
    """
    def __init__(self):
        # Pygame window-related variables
        self.events = pygame.event.get()
        self.__running = False
        self.screen = pygame.display.set_mode(Constants.SCREEN_SIZE, pygame.DOUBLEBUF)
        ASSET_LOADER.load()  # Triggers delayed asset loading

        # Load levels from file
        self.levels = []
        self.__load_levels()

        # Load score and completion data from file
        self.score = 0
        self.completed = [False] * len(self.levels)
        self.__load_player_data()

        self.menu_state: MenuStates = MenuStates.GAME  # What state is the menu in
        self.__managers: list[Optional[Manager]] = [None] * len(MenuStates)  # Instances of menu state managers
        self.__switch_params: dict = dict()  # A tuple of parameters
        self.__is_switched = False  # Indicates that state has been changed

    def __load_player_data(self):
        with open("data.json", "r") as file:
            loaded = json.load(file)
            if not loaded["highest"] == -1:
                for x in range(loaded["highest"] + 1):
                    self.completed[x] = True
            self.score = loaded["score"]

    def __load_levels(self):
        with open("level.json", "r") as file:
            self.levels = json.load(file)

    def get_level_json_at_index(self, idx: int) -> dict:
        return self.levels[idx]

    def __save_game(self):
        with open("data.json", "w") as file:
            completed = len([x for x in self.completed if x]) - 1
            json.dump({"highest": completed, "score": self.score}, file)

    def switch_state(self, new_state: MenuStates, param_dict=dict()):
        """Used by manager classes to change screens"""
        self.menu_state = new_state
        self.__switch_params = param_dict
        self.__is_switched = True

    def __update_manager(self):
        """Assumes manager index was updated to new one"""
        self.__is_switched = False
        if self.__managers[self.menu_state.value] is None or (not self.__managers[self.menu_state.value].do_persist()):
            # Generate a new instance with passed filtered dict of keyword params
            clss: type = STATE_TO_CLASS[self.menu_state]
            self.__managers[self.menu_state.value] = clss(self, **{k: self.__switch_params[k] for k in self.__switch_params if k in list(inspect.signature(clss).parameters.keys())})
            self.__switch_params = dict()

    def handle_exit(self):
        """Called when main loop finishes under any circumstances"""
        self.__save_game()

    def stop_game(self):
        """Set flag to stop game on next loop iteration"""
        self.__running = False

    def start_game(self):
        """Start the main game loop and run it until game quits"""
        self.__running = True  # Set game to running
        clock = pygame.time.Clock()  # FPS clock
        last_fps_show = 0
        self.__update_manager()  # Set up first menu state

        while self.__running:
            self.screen.fill((111, 80, 51))  # Clear screen
            self.events = pygame.event.get()  # Get events

            # Checks for window closure
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.__running = False

            # Run current manager and update the instance if the state changed
            self.__managers[self.menu_state.value].run(self.screen, self)
            if self.__is_switched:
                self.__update_manager()

            pygame.display.update()  # Update display

            # Show FPS counter
            last_fps_show += 1
            if last_fps_show == 30:  # every 30th frame:
                fps = clock.get_fps()
                pygame.display.set_caption("Silverball v.2.0" + "   FPS: " + str(fps))
                last_fps_show = 0

            # fps max
            clock.tick(150)

        self.handle_exit()  # Safely terminate (i.e save game)


    # def start_game(self, idx):
    #     self.load_levels()
    #     self.game = Level.Level(self.levels[idx])
    #     self.menu_state = 'game'
