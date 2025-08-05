import pygame as pg
import random


class Zombie(pg.sprite.Sprite):
    def __init__(self):
        super(Zombie, self).__init__()
        self.image = pg.image.load('material/images/Zombie_0.png').convert_alpha()
        self.images = [pg.image.load('material/images/Zombie_{}.png'.format(i)).convert_alpha() for i in range(22)]
        self.die_images = [pg.image.load('material/images/ZombieDie_{}.png'.format(i)).convert_alpha() for i in range(10)]
        self.attack_images = [pg.image.load('material/images/ZombieAttack_{}.png'.format(i)) for i in range(21)]

        self.rect = self.images[0].get_rect()
        self.rect.top = 50 + random.randrange(0, 5) * 120
        self.rect.left = 1200
        self.speed = 1
        self.energy = 10
        self.die_time = 0
        self.attack = 2

        self.is_eating = False
        self.is_alive = True

    def update(self, *args):
        if self.energy > 0:
            if self.is_eating:
                self.image = self.attack_images[args[0] % len(self.attack_images)]
            else:
                self.image = self.images[args[0] % len(self.images)]
            if self.rect.left > 250 and not self.is_eating:
                self.rect.left -= self.speed
        else:
            if self.die_time < 20:
                self.image = self.die_images[int(self.die_time/2)]
                self.die_time += 1
            elif self.die_time > 40:
                self.kill()
            else:
                self.die_time += 1
                self.is_alive = False
