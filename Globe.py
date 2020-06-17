import pygame
import Menu

running = True
events = None
MENU = None


def start_app():
    global MENU, events
    MENU = Menu.Menu()

    events = pygame.event.get()
