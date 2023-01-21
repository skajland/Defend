import math
import random
import pygame
from pygame import mixer
import functions


def from_witch_side_spawn():
    if functions.round_number <= 7:
        x = 0
    else:
        x = 300
    result_border = random.randint(1, 4)
    # left border
    if result_border == 1:
        y = random.randint(0, 950)
        x = random.randint(-584 - x, -128)
        return x, y
    # right border
    if result_border == 2:
        y = random.randint(0, 950)
        x = random.randint(1314, 1770 + x)
        return x, y
    # top border
    if result_border == 3:
        y = random.randint(-584 - x, -128)
        x = random.randint(0, 1250)
        return x, y
    # bottom border
    else:
        y = random.randint(1028, 1484 + x)
        x = random.randint(0, 1250)
        return x, y


class Zombie:

    def __init__(self, zombie_img_load, zombie_speed, health):
        self.zombie_img = []

        self.zombie_rect = []

        self.zombie_x = []
        self.zombie_y = []

        self.zombie_count = 0

        self.angle = []
        self.zombie_y_change = []
        self.zombie_x_change = []

        self.health = []

        self.how_much_zombies_spawn = 0

        self.set_health = health
        self.zombie_img_load = zombie_img_load
        self.zombie_speed = zombie_speed

    def create_zombie(self):
        self.zombie_img.append(self.zombie_img_load)

        x, y = from_witch_side_spawn()

        self.health.append(self.set_health)
        self.zombie_x.append(x)
        self.zombie_y.append(y)

        self.zombie_count += 1

        self.angle.append(0)

        self.zombie_rect.append(self.zombie_img[-1].get_rect())

        self.zombie_y_change.append(0)
        self.zombie_x_change.append(0)

    def render(self, screen):
        for z in range(self.zombie_count):
            rotated_img = pygame.transform.rotate(self.zombie_img[z], math.degrees(-self.angle[z]) - 90)
            screen.blit(rotated_img, (self.zombie_x[z] - rotated_img.get_width() / 2,
                                      self.zombie_y[z] - rotated_img.get_height() / 2))  # renders and centers

    def move(self, dt):
        for z in range(self.zombie_count):
            dy = 475.5 - self.zombie_y[z]  # Zombie goes to base y
            dx = 626.5 - self.zombie_x[z]  # Zombie goes to base x

            self.angle[z] = math.atan2(dy, dx)

            self.zombie_y_change[z] = math.sin(self.angle[z]) * self.zombie_speed / 10  # moves towards the base
            self.zombie_x_change[z] = math.cos(self.angle[z]) * self.zombie_speed / 10  # moves towards the base

            self.zombie_y[z] += self.zombie_y_change[z] * dt  # rotates towards the base
            self.zombie_x[z] += self.zombie_x_change[z] * dt  # rotates towards the base

    def collision(self, player_rect):
        for z in range(self.zombie_count):
            if self.zombie_rect[z].colliderect(player_rect):  # collision with player
                functions.lost_game = True

    def collision_update(self):
        for z in range(self.zombie_count):
            self.zombie_rect[z].centery = self.zombie_y[z]  # updates collision y and centers y
            self.zombie_rect[z].centerx = self.zombie_x[z]  # updates collision x and centers x

    def zombie_delete(self, z):
        self.zombie_img.pop(z)

        self.zombie_x.pop(z)
        self.zombie_y.pop(z)

        self.zombie_count -= 1

        self.angle.pop(z)

        self.zombie_rect.pop(z)

        self.health.pop(z)

        self.zombie_y_change.pop(z)
        self.zombie_x_change.pop(z)

    def zombie_clearer(self):
        self.zombie_img.clear()

        self.zombie_x.clear()
        self.zombie_y.clear()

        self.zombie_count = 0

        self.angle.clear()

        self.zombie_rect.clear()

        self.health.clear()

        self.zombie_y_change.clear()
        self.zombie_x_change.clear()

    def check_health(self):
        kill_list = []

        for z in range(self.zombie_count):
            if self.health[z] <= 0:
                kill_list.append(z)

        if len(kill_list) > 0:
            self.zombie_delete(kill_list[0])
            functions.score += 1
            random_number = random.randint(0, 3)
            if random_number == 0:
                mixer.Sound('Sounds/ZombieDied.mp3').play(0)
            elif random_number == 1:
                mixer.Sound('Sounds/ZombieDied2.mp3').play(0)
            elif random_number == 2:
                mixer.Sound('Sounds/ZombieDied3.mp3').play(0)
            else:
                mixer.Sound('Sounds/ZombieDied4.mp3').play(0)
