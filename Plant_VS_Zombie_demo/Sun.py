import pygame as pg
import random


class Sun(pg.sprite.Sprite):
    def __init__(self, sun_rect):
        '''
        Sun
        :param rect: position of sunflower
        '''
        super(Sun, self).__init__()
        self.image = pg.image.load('material/images/Sun_1.png').convert_alpha()
        self.images = [pg.image.load('material/images/Sun_{:d}.png'.format(i)).convert_alpha() for i in range(1, 18)]

        self.rect = self.images[0].get_rect()

        offset_top = random.randint(-50, 50)
        offset_left = random.randint(-50, 50)
        self.rect.top = sun_rect.top + offset_top
        self.rect.left = sun_rect.left + offset_left

    def update(self, *args):
        self.image = self.images[args[0] % len(self.images)]
