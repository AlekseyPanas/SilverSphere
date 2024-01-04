import pygame
import Constants
import Sprite
import random
import signal
import Menu


pygame.display.set_mode(Constants.SCREEN_SIZE)
Constants.convert()
m = Menu.Menu()

signal.signal(signal.SIGINT, m.handle_exit)
signal.signal(signal.SIGTERM, m.handle_exit)

m.start_game()
