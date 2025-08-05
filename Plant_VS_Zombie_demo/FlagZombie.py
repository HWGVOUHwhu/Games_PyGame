import pygame as pg
from Zombie import Zombie


class FlagZombie(Zombie):
    def __init__(self):
        super(FlagZombie, self).__init__()
        self.image = pg.image.load('material/images/FlagZombie_0.png').convert_alpha()
        self.images = [pg.image.load('material/images/FlagZombie_{}.png'.format(i)).convert_alpha() for i in range(12)]
        self.attack_images = [pg.image.load('material/images/ZombieAttack_{}.png'.format(i)) for i in range(11)]
        # self.rect = self.images[0].get_rect()
        # self.rect.top = 50 + random.randrange(0, 5) * 125
        # self.rect.left = 1200
        self.speed = 2
        self.energy = 8
        self.attack = 1

    # def update(self, *args):
    #     if self.energy > 0:
    #         self.image = self.images[args[0] % len(self.images)]
    #         if self.rect.left > 250:
    #             self.rect.left -= self.speed
    #     else:
    #         self.kill()
