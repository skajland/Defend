import pygame

import functions
from bullet import Bullet
from player import Player
from zombie import Zombie

pygame.init()

p1 = Player(625, 475)
b1 = Bullet(50)
z1 = (Zombie(pygame.image.load('Pictures/Zombies/Zombie.png'), 1, 50))
z2 = (Zombie(pygame.image.load('Pictures/Zombies/ZombieSlow.png'), 0.85, 200))
z3 = (Zombie(pygame.image.load('Pictures/Zombies/ZombieFast.png'), 3, 50))
z4 = (Zombie(pygame.image.load('Pictures/Zombies/ZombieHidden.png'), 1.25, 100))
z5 = (Zombie(pygame.image.load('Pictures/Zombies/ZombieBoss.png'), 0.7, 450))
z6 = (Zombie(pygame.image.load('Pictures/Zombies/SmallZombie.png'), 1.5, 150))
zombies1 = (z4, z1, z2, z3, z5, z6)

color = (195, 195, 195)


def zombies(zombie, delta):
    zombie.move(delta)
    zombie.collision_update()
    zombie.collision(p1.player_rect)
    zombie.check_health()
    functions.start_round(zombies1)


def main_game(screen, dt):
    global color
    screen.fill(color)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            functions.stop = True
        p1.shoot(events, b1, 2.25)

    if functions.lost_game:
        functions.lose_screen(screen, dt)

        color = (200, functions.g, functions.b)
    else:
        color = (195, 195, 195)

        p1.rotate()  # rotates gun
        p1.collision_update()

        b1.move(dt)
        b1.borders(-1048, 2294, -1048, 2294)
        b1.collision_update()

        for z in range(len(zombies1)):
            b1.collision(zombies1[z])
            zombies(zombies1[z], dt)

        for z in range(len(zombies1)):
            zombies1[z].render(screen)

        functions.score_text(screen)
        functions.round_text(screen)

        b1.render(screen)
        p1.render(screen)

    pygame.display.flip()
