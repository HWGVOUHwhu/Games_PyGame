import pygame as pg


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, pipes_image, upwards=True):
        super(Pipe, self).__init__()
        if upwards:
            self.image = pipes_image[0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        else:
            self.image = pipes_image[1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

        self.x_vel = -4
        self.scored = False
        self.upwards = upwards

    def update(self):
        self.rect.x += self.x_vel
