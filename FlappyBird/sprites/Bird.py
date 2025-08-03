import pygame as pg


class Bird(pg.sprite.Sprite):
    def __init__(self, x, y, bird_images, floor_y):
        super(Bird, self).__init__()
        self.idx = 0
        self.repeat = 3
        self.floor_y = floor_y
        self.frames = [0] * self.repeat + [1] * self.repeat + [2] * self.repeat + [1] * self.repeat
        self.images = bird_images
        self.image = bird_images[self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y_val = -10
        self.max_y_val = 10
        self.gravity = 1

        self.rotate = 45
        self.max_rotate = -20
        self.rotate_vel = -3

        self.y_val_flap = -10
        self.rotate_flap = 45

        self.died = False

    def update(self, flap=False):

        if flap:
            self.y_val = self.y_val_flap
            self.rotate = self.rotate_flap

        self.y_val = min(self.y_val + self.gravity, self.max_y_val)
        self.rect.y += self.y_val

        self.rotate = max(self.rotate + self.rotate_vel, self.max_rotate)

        self.idx = (self.idx + 1) % len(self.frames)
        self.image = self.images[self.frames[self.idx]]
        self.image = pg.transform.rotate(self.image, self.rotate)

    def go_die(self):
        if self.rect.y < self.floor_y:
            self.rect.y += self.max_y_val
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pg.transform.rotate(self.image, self.rotate)
        else:
            self.died = False
