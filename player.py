import math
import pygame
from pygame import mixer

import functions


class Player:

    def __init__(self, x, y):
        self.player_img = pygame.image.load('Pictures/PlayerBase.png')
        self.player_gun_img = pygame.image.load('Pictures/PlayerGun.png')

        self.player_x = x
        self.player_y = y
        self.player_rect = self.player_img.get_rect()

        self.angle = 0

    def render(self, screen):
        # player base
        screen.blit(self.player_img, (self.player_x - self.player_img.get_width() / 2, self.player_y - self.player_img.get_height() / 2))
        # Rotate the image and this is player gun
        player_gun_img_rot = pygame.transform.rotate(self.player_gun_img, -math.degrees(self.angle) - 90)
        screen.blit(player_gun_img_rot, (self.player_x - player_gun_img_rot.get_width() / 2, self.player_y - player_gun_img_rot.get_height() / 2))

    def rotate(self):
        # Get the mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the image and the mouse
        dx = mouse_x - self.player_x
        dy = mouse_y - self.player_y
        self.angle = math.atan2(dy, dx)

    def shoot(self, events, b, speed):
        # clicked left mouse button to shoot
        if events.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and not b.bullet_count >= 3 and not functions.lost_game:
                b.shoot(self.angle, self.player_y-24, self.player_x-24, speed)
                mixer.Sound('Sounds/ShootSound.mp3').play(0)

    def collision_update(self):
        self.player_rect.centery = self.player_y  # updates collision y and centers y
        self.player_rect.centerx = self.player_x  # updates collision x and centers x
