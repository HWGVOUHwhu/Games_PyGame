import pygame as pg


class Sunflower(pg.sprite.Sprite):
    def __init__(self, last_time):
        super(Sunflower, self).__init__()
        self.image = pg.image.load('material/images/Sunflower_00.png').convert_alpha()
        self.images = [pg.image.load('material/images/Sunflower_{:02d}.png'.format(i)).convert_alpha() for i in range(0, 13)]

        self.rect = self.images[0].get_rect()
        # self.rect.top = 225
        # self.rect.left = 325
        self.energy = 200
        self.zombies = set()

        self.last_time = last_time

    def update(self, *args):
        for zombie in self.zombies:
            if zombie.is_alive:
                self.energy -= zombie.attack

        if self.energy <= 0:
            for zombie in self.zombies:
                zombie.is_eating = False
            self.kill()
        else:
            self.image = self.images[args[0] % len(self.images)]

