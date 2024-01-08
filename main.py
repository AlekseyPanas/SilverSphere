from __future__ import annotations
import pygame
import Constants
import signal
import Menu
import importlib

pygame.display.set_mode(Constants.SCREEN_SIZE)
m = Menu.Menu()

signal.signal(signal.SIGINT, m.stop_game)
signal.signal(signal.SIGTERM, m.stop_game)

m.start_game()
