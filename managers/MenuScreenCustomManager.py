from __future__ import annotations
import pygame
from managers.Managers import ASSET_LOADER, register_assets, PreAsset
from managers.MenuScreenManager import MenuScreenManager
import Menu
import Button
import Constants
import os
from Constants import path2asset, cscale
import json
from game.LevelData import LevelData, BoxData, EnemyData
from dataclasses import dataclass
from Typefield import Field
import shutil


@dataclass
class Page:
    level_buttons: list[Button]
    edit_buttons: list[Button]


@register_assets(ASSET_LOADER)
class MenuScreenCustomManager(MenuScreenManager):
    CUSTOM_LEVELS_FILENAME = "customlevels.json"

    BUTTONS_START_TOPLEFT = cscale(80, 240)
    BUTTON_SIZE = cscale(200, 50)

    def __init__(self, menu: Menu):
        super().__init__(menu)
        # Generate file if not exist
        if self.CUSTOM_LEVELS_FILENAME not in os.listdir(Constants.ROOT_PATH):
            with open(Constants.path2file(self.CUSTOM_LEVELS_FILENAME), "w") as file:
                json.dump([], file)

        # Load file
        with open(Constants.path2file(self.CUSTOM_LEVELS_FILENAME), "r") as file:
            level_data = json.load(file)

        # Parses levels into dataclasses
        self.custom_levels: list[LevelData] = [LevelData.from_dict(d) for d in level_data]

        # Pagination and level selection
        self.__pages: list[Page] = []
        self.__cur_page = 0
        self.__generate_pages()

        self.__next_page_button = Button.Button(cscale(270, 190), cscale(30, 30), None, True, (0, 0, 0), (0, 0, 0), (100, 100, 100), ">", cscale(2), Constants.get_arial(cscale(20)))
        self.__prev_page_button = Button.Button(cscale(240, 190), cscale(30, 30), None, True, (0, 0, 0), (0, 0, 0), (100, 100, 100), "<", cscale(2), Constants.get_arial(cscale(20)))
        self.__back_button = Button.Button(cscale(340, 187), cscale(70, 40), None, True, (0, 0, 0), (0, 0, 0), (190, 150, 150), "Back", cscale(2), Constants.get_arial(cscale(22)))
        self.__new_level_button = Button.Button(cscale(780, 330), cscale(40, 40), None, True, (0, 0, 0), (0, 0, 0), (100, 220, 100), "+", cscale(2), Constants.get_arial(cscale(22)))

        s = pygame.Surface((100, 50), pygame.SRCALPHA, 32)
        pygame.draw.line(s, (70, 70, 120), (0, 46), (100, 46), 3)
        self.__level_name_typefield = Field(cscale(700, 280), cscale(200), Constants.get_arial(cscale(20)), s, color=(0, 0, 0), allowed_symbols={chr(a) for a in list(range(65, 91)) + list(range(97, 123))}.union({" "}))

    def save_levels(self):
        """Save self.custom_levels to file"""
        p = Constants.path2file(self.CUSTOM_LEVELS_FILENAME)
        shutil.copy(p, Constants.path2file(self.CUSTOM_LEVELS_FILENAME + ".bak"))
        with open(p, "w") as file:
            json.dump([s.to_dict() for s in self.custom_levels], file)

    def add_level(self, level: LevelData):
        """Add a new custom level, save the levels, and regenerate buttons"""
        self.custom_levels.append(level)
        self.save_levels()
        self.__generate_pages()

    def __generate_pages(self):
        """Generate buttons and page data based on self.custom_levels"""
        self.__pages = []
        self.__cur_page = 0

        for i in range(len(self.custom_levels)):
            page_idx = i // 6
            level_idx = i % 6
            if page_idx >= len(self.__pages):
                self.__pages.append(Page([], []))
            self.__pages[page_idx].level_buttons.append(
                Button.Button((self.BUTTONS_START_TOPLEFT[0], self.BUTTONS_START_TOPLEFT[1] + (self.BUTTON_SIZE[1] + cscale(20)) * level_idx), self.BUTTON_SIZE, None, True, (0, 0, 0), (0, 0, 0),
                              (level_idx * 20 + 100, level_idx * 20 + 100, 200), self.custom_levels[i].name.upper(),
                              cscale(2), Constants.get_arial(cscale(15)))
            )
            self.__pages[page_idx].edit_buttons.append(
                Button.Button((self.BUTTONS_START_TOPLEFT[0] + cscale(30) + self.BUTTON_SIZE[0], self.BUTTONS_START_TOPLEFT[1] + (self.BUTTON_SIZE[1] + cscale(20)) * level_idx),
                              cscale(100, 50), None, True, (0, 0, 0), (0, 0, 0),
                              (50, 200, 50), "EDIT",
                              cscale(2), Constants.get_arial(cscale(15)))
            )

    def run_menu_foreground(self, screen: pygame.Surface, menu: Menu):
        msps = pygame.mouse.get_pos()

        # Draw text
        page_text = Constants.get_impact(cscale(30)).render(f"Page {self.__cur_page + 1} of {len(self.__pages)}", True, (0, 0, 0))
        screen.blit(page_text, page_text.get_rect(topleft=cscale(80, 187)))

        name_text = Constants.get_impact(cscale(25)).render("Enter New Level Name:", True, (0, 0, 0))
        screen.blit(name_text, name_text.get_rect(center=cscale(800, 250)))

        if len(self.__pages):
            for i in range(len(self.__pages[self.__cur_page].level_buttons)):
                level_idx = self.__cur_page * 6 + i

                # Draw button
                self.__pages[self.__cur_page].level_buttons[i].draw_and_hover(screen, msps)
                self.__pages[self.__cur_page].edit_buttons[i].draw_and_hover(screen, msps)

                # Check clicks
                for e in menu.events:
                    if e.type == pygame.MOUSEBUTTONUP:
                        if self.__pages[self.__cur_page].level_buttons[i].is_clicked(e.pos):
                            menu.switch_state(Menu.MenuStates.GAME, {"level_json": self.custom_levels[level_idx].to_dict(), "level_idx": None})
                        elif self.__pages[self.__cur_page].edit_buttons[i].is_clicked(e.pos):
                            menu.switch_state(Menu.MenuStates.EDITOR,
                                              {"custom_levels_manager": self,
                                               "level_data_ref": self.custom_levels[level_idx]})

        self.__prev_page_button.draw_and_hover(screen, msps)
        self.__back_button.draw_and_hover(screen, msps)
        self.__next_page_button.draw_and_hover(screen, msps)
        self.__new_level_button.draw_and_hover(screen, msps)

        self.__level_name_typefield.draw_handler(screen)

        for e in menu.events:
            self.__level_name_typefield.event_handler(e)
            if e.type == pygame.MOUSEBUTTONUP:
                if self.__next_page_button.is_clicked(e.pos):
                    if self.__cur_page < len(self.__pages) - 1:
                        self.__cur_page += 1
                elif self.__prev_page_button.is_clicked(e.pos):
                    if self.__cur_page > 0:
                        self.__cur_page -= 1
                elif self.__back_button.is_clicked(e.pos):
                    menu.switch_state(Menu.MenuStates.MAIN)
                elif self.__new_level_button.is_clicked(e.pos):
                    if not all(c == " " for c in self.__level_name_typefield.text):
                        new_lvl_name = self.__level_name_typefield.text.strip().upper()
                        self.add_level(LevelData.generate_default(new_lvl_name))
                        self.__cur_page = len(self.__pages) - 1
