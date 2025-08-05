import pygame as pg


class WallNut(pg.sprite.Sprite):
    def __init__(self):
        super(WallNut, self).__init__()
        self.image = pg.image.load('material/images/WallNut_00.png').convert_alpha()
        self.images = [pg.image.load('material/images/WallNut_{:02d}.png'.format(i)).convert_alpha() for i in range(0, 13)]
        self.crackedImgs = [
            pg.transform.smoothscale(pg.image.load('material/images/Wallnut_body.png').convert_alpha(),
                                     (self.image.get_rect().width, self.image.get_rect().height)),
            pg.transform.smoothscale(pg.image.load('material/images/Wallnut_cracked1.png').convert_alpha(),
                                     (self.image.get_rect().width, self.image.get_rect().height)),
            pg.transform.smoothscale(pg.image.load('material/images/Wallnut_cracked2.png').convert_alpha(),
                                     (self.image.get_rect().width, self.image.get_rect().height)),
        ]

        self.rect = self.images[0].get_rect()
        # self.rect.top = 350
        # self.rect.left = 325
        self.energy = 3 * 500
        self.zombies = set()

    def update(self, *args):
        for zombie in self.zombies:
            if zombie.is_alive:
                self.energy -= zombie.attack

        if self.energy <= 0:
            for zombie in self.zombies:
                zombie.is_eating = False
            self.kill()
        elif self.energy == 3 * 500:
            self.image = self.images[args[0] % len(self.images)]
        elif 2 * 500 <= self.energy < 3 * 500:
            self.image = self.crackedImgs[0]
        elif 1 * 500 <= self.energy < 2 * 500:
            self.image = self.crackedImgs[1]
        elif self.energy < 1 * 500:
            self.image = self.crackedImgs[2]
