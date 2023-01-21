import math
import random

import pygame
from pygame import mixer
pygame.init()

score = 0

round_number = 0

lost_game = False
main_menu_running = True
main_game_running = True
stop = False

g = 195
b = 195
r_b = 200
g_b = 195
b_b = 195


def font(this_font, size):
    return pygame.font.Font(this_font, size)


def rotate(img, rot):
    orig_rect = img.get_rect()
    rot_image = pygame.transform.rotate(img, math.degrees(rot))
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    return rot_image.subsurface(rot_rect).copy()


def button_create(button, x, y, dt, screen):
    global r_b, g_b, b_b, stop
    button_rect = button.get_rect()
    button_rect.y, button_rect.x = y, x
    mouse_pos = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(mouse_pos, (8, 8))
    speed = 0.035
    box = button_rect.copy()
    if mouse_rect.colliderect(button_rect):
        pygame.draw.rect(screen, (r_b, g_b, b_b), box, 128)
        if r_b < 210:  # when hovered over a button
            r_b += speed * dt
            g_b += speed * dt
            b_b += speed * dt
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                stop = True

            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mixer.Sound('Sounds/ButtonSound.mp3').play()
                    return False
    else:
        pygame.draw.rect(screen, (r_b, g_b, b_b), box, 128)
        if r_b > 200:  # when stopped hovering over a button
            r_b -= speed * dt
        if g_b > 42.5:
            g_b -= speed * dt
        if b_b > 42.5:
            b_b -= speed * dt

    return True


def lose_screen(screen, dt):
    global g, b, main_game_running
    render_font = font('freesansbold.ttf', 64).render("You Died!", True, (255, g, b))
    render_font_score = font('freesansbold.ttf', 48).render("Your score: " + str(score), True, (255, g, b))
    render_font_again = font('freesansbold.ttf', 64).render("Main Menu", True, (255, g, b),)
    x = screen.get_width() / 2 - render_font_again.get_width() / 2
    y = screen.get_height() / 2 - render_font_again.get_height() / 2
    main_game_running = button_create(render_font_again, x, y, dt, screen)
    screen.blits(((render_font, (screen.get_width() / 2 - render_font.get_width() / 2, render_font.get_height() / 2)),
                  (render_font_score, (screen.get_width() / 2 - render_font_score.get_width() / 2, render_font.get_height() / 2 + render_font_score.get_height() + 15)),
                  (render_font_again, (x, y))))

    if g > 42.5 or b > 42.5:
        mixer.Sound('Sounds/YouDied.mp3').play()
        g -= 0.035 * dt
        b -= 0.035 * dt


def score_text(screen):
    score_y = 10
    render_font = font('freesansbold.ttf', 64).render(str(score), True, (0, 0, 0))
    score_x = screen.get_width() / 2 - render_font.get_width() / 2
    screen.blit(render_font, (score_x, score_y))


def round_text(screen):
    round_x = 10
    round_y = 10

    render_font = font('freesansbold.ttf', 64).render(str(round_number), True, (0, 0, 0))
    screen.blit(render_font, (round_x, round_y))


def round_system(zombies):
    global round_number

    round_number += 1

    if round_number >= 5:
        rng = random.randint(0, 5)
        if rng == 0:
            zombies[0].how_much_zombies_spawn += 1
        elif rng == 1:
            zombies[1].how_much_zombies_spawn += 1
        elif rng == 2:
            zombies[2].how_much_zombies_spawn += 1
        elif rng == 3:
            zombies[3].how_much_zombies_spawn += 1
        elif rng == 4:
            zombies[4].how_much_zombies_spawn += 1
        elif rng == 5:
            zombies[5].how_much_zombies_spawn += 1
    else:
        zombies[1].how_much_zombies_spawn += 1


def start_round(zombies):

    all_zombies = 0

    for z in zombies:
        all_zombies += z.zombie_count

    if all_zombies <= 0:
        round_system(zombies)

        for z in zombies:
            for _ in range(z.how_much_zombies_spawn):
                z.create_zombie()


def reset_game(zombies, main_menu, main_game):
    global lost_game, main_game_running, main_menu_running, round_number, score, g, b, g_b, b_b, r_b
    lost_game = False
    main_menu.b1.bullet_clearer()
    main_menu.shot_exit_button = 0
    main_game.b1.bullet_clearer()
    main_menu_running = True
    main_game_running = True
    for z in zombies:
        z.how_much_zombies_spawn = 0
        z.zombie_clearer()
    round_number = 0
    score = 0
    g = 195
    b = 195
    g_b = 195
    b_b = 195
    r_b = 200
    main_menu.x_exit_change = 0
    main_menu.x_exit = 139
