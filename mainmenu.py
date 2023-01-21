import random

import pygame
from pygame import mixer
from player import Player
from bullet import Bullet
import functions

pygame.init()

p1 = Player(1150, 475)
b1 = Bullet(50)

render_font = functions.font('freesansbold.ttf', 164).render("DEFEND", True, (0, 0, 0))  # Makes Title
render_font_play = functions.font('freesansbold.ttf', 96).render("Play", True, (0, 0, 0))  # Makes Play
render_font_exit = functions.font('freesansbold.ttf', 96).render("Exit", True, (0, 0, 0))  # Makes Exit

play_rect = render_font_play.get_rect()  # For Collision
exit_rect = render_font_exit.get_rect()  # For Collision

x_exit = 625 - 150 - render_font.get_width() / 2
x_exit_change = 0

r = 195
g = 195
b = 195

dt = 0

shot_exit_button = 0

box = play_rect.copy()


def render_all_text_main_screen(screen):
    global x_exit
    collision(screen)
    # Renders on screen all texts
    x_play = screen.get_width() / 2 - 150 - render_font.get_width() / 2

    x_exit += x_exit_change * dt
    screen.blits(((render_font, (screen.get_width() / 2 - 150 - render_font.get_width() / 2, 0)), (render_font_play, (x_play, 300)), (render_font_exit, (x_exit, 600))))

    play_rect.x, play_rect.y = x_play, 300
    exit_rect.x, exit_rect.y = x_exit, 600


def main_menu(screen, delta):
    global dt

    screen.fill((195, 195, 195))

    dt = delta

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            functions.main_menu_running = False
            functions.stop = True
        p1.shoot(events, b1, 3.25)
    p1.rotate()  # rotates gun

    b1.collision_update()
    b1.move(delta)
    b1.borders(-128, screen.get_width() + 128, -128, screen.get_height() + 128)

    b1.render(screen)

    render_all_text_main_screen(screen)

    p1.render(screen)

    pygame.display.flip()


def collision(screen):
    global r, g, b, box, shot_exit_button, x_exit_change, x_exit
    mouse_pos = pygame.mouse.get_pos()

    mouse_rect = pygame.Rect(mouse_pos, (8, 8))

    mouse_rect.y = mouse_pos[1] - mouse_rect.size[1] / 2
    mouse_rect.x = mouse_pos[0] - mouse_rect.size[0] / 2

    speed = 0.075

    if mouse_rect.colliderect(play_rect):
        box = play_rect.copy()
        if r < 210:  # when hovered over a button
            r += speed * dt
            g += speed * dt
            b += speed * dt
    elif mouse_rect.colliderect(exit_rect):
        box = exit_rect.copy()
        if r < 210:  # when hovered over a button
            r += speed * dt
            g += speed * dt
            b += speed * dt
    else:
        if r > 195:  # when stopped hovering over a button
            r -= speed * dt
            g -= speed * dt
            b -= speed * dt
    i = -1  # witch bullet to delete

    for bullet in b1.bullet_rect:
        i += 1

        if bullet.colliderect(play_rect):  # colliding with play button
            functions.main_menu_running = False
            mixer.Sound('Sounds/ButtonSound.mp3').play()
        elif bullet.colliderect(exit_rect):  # colliding with exit button
            shot_exit_button += 1
            b1.bullet_delete(i)

            if shot_exit_button >= 3:  # shoot two times
                functions.stop = True

    if shot_exit_button == 1:
        mixer.Sound('Sounds/ButtonSound.mp3').play()
        shot_exit_button += 1

        if random.randint(0, 1) == 0:
            x_exit_change = 0.07
        else:
            x_exit_change = -0.07

    elif shot_exit_button > 1:
        if x_exit <= 133:
            x_exit_change = 0.07
        elif x_exit >= 145:
            x_exit_change = -0.07

    pygame.draw.rect(screen, (r, g, b), box, 64)
