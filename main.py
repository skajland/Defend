import pygame
import time

import mainmenu
import maingame
import functions
pygame.init()

screen = pygame.display.set_mode((1250, 950))

# This is my second game in pygame, I'm 13 years old when I created this in 2022 - 2023

pygame.display.set_caption("Defend")

prev_time = time.time()  # previous time
while not functions.stop:
    while functions.main_menu_running and not functions.stop:
        # delta time
        now = time.time()
        dt = now - prev_time
        dt *= 1000  # increased delta time speed
        prev_time = time.time()  # previous time updating

        mainmenu.main_menu(screen, dt)

    while functions.main_game_running and not functions.stop:
        # delta time
        now = time.time()
        dt = now - prev_time
        dt *= 1000  # increased delta time speed
        prev_time = time.time()  # previous time updating
        maingame.main_game(screen, dt)

    if not functions.stop:
        functions.reset_game(maingame.zombies1, mainmenu, maingame)
