import math
import functions
import pygame


class Bullet:
    def __init__(self, damage):
        self.bullet_image = []

        self.bullet_count = 0

        self.bullet_x = []
        self.bullet_y = []

        self.bullet_rect = []

        self.bullet_y_change = []
        self.bullet_x_change = []

        self.damage = damage

        self.shot = []

        self.angle = []

    def spawn_bullet(self):
        self.bullet_image.append(pygame.image.load('Pictures/PlayerBullet.png'))

        self.bullet_count += 1

        self.bullet_x.append(625)
        self.bullet_y.append(475)

        self.bullet_y_change.append(0.0)
        self.bullet_x_change.append(0.0)
        self.bullet_rect.append(self.bullet_image[-1].get_rect())

        self.shot.append(False)

        self.angle.append(0.0)

    def render(self, screen):
        # if shot render bullet
        for b in range(self.bullet_count):
            if self.shot:
                rotated_img = functions.rotate(self.bullet_image[b], -self.angle[b])
                screen.blit(rotated_img, (self.bullet_x[b], self.bullet_y[b]))

    def shoot(self, angle, y, x, speed):
        self.spawn_bullet()
        self.angle[-1] = math.radians(math.degrees(angle) + 90)

        self.bullet_y[-1] = y
        self.bullet_x[-1] = x

        self.bullet_y[-1] += math.sin(angle) * 100
        self.bullet_x[-1] += math.cos(angle) * 100
        # running once
        if not self.shot[-1]:
            self.bullet_y_change[-1] = math.sin(angle) * speed / 5
            self.bullet_x_change[-1] = math.cos(angle) * speed / 5
        self.shot[-1] = True

    def move(self, dt):
        for b in range(self.bullet_count):
            if self.shot[b]:
                # updating bullet movement y
                self.bullet_y[b] += self.bullet_y_change[b] * dt
                # updating bullet movement x
                self.bullet_x[b] += self.bullet_x_change[b] * dt

    def borders(self, left_border, right_border, top_border, bottom_border):
        kill_list = []
        for b in range(self.bullet_count):
            if self.shot[b]:
                # left border
                if self.bullet_x[b] <= left_border:
                    kill_list.append(b)
                # right border
                elif self.bullet_x[b] >= right_border:
                    kill_list.append(b)
                # top border
                elif self.bullet_y[b] <= top_border:
                    kill_list.append(b)
                # bottom border
                elif self.bullet_y[b] >= bottom_border:
                    kill_list.append(b)
        if len(kill_list) > 0:
            self.bullet_delete(kill_list[0])

    def bullet_delete(self, b):
        # deletes the bullet
        self.bullet_count -= 1

        self.bullet_image.pop(b)

        self.bullet_x.pop(b)
        self.bullet_y.pop(b)

        self.bullet_y_change.pop(b)
        self.bullet_x_change.pop(b)

        self.bullet_rect.pop(b)

        self.shot.pop(b)

        self.angle.pop(b)

    def bullet_clearer(self):
        self.bullet_count = 0

        self.bullet_image.clear()

        self.bullet_x.clear()
        self.bullet_y.clear()

        self.bullet_y_change.clear()
        self.bullet_x_change.clear()

        self.bullet_rect.clear()

        self.shot.clear()

        self.angle.clear()

    def collision(self, z1):
        bullet_kill_list = []
        for b in range(self.bullet_count):
            for z in range(z1.zombie_count):

                if self.bullet_rect[b].colliderect(z1.zombie_rect[z]):
                    bullet_kill_list.append(b)
                    z1.health[z] -= self.damage

        if len(bullet_kill_list) > 0:
            self.bullet_delete(bullet_kill_list[0])

    def collision_update(self):
        for b in range(self.bullet_count):
            self.bullet_rect[b].y = self.bullet_y[b]  # updates collision y
            self.bullet_rect[b].x = self.bullet_x[b]  # updates collision x
