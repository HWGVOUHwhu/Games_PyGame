import pygame as pg

BLACK = (0, 0, 0)


class Bullet(pg.sprite.Sprite):
    def __init__(self, pea_rect, back_size):
        super(Bullet, self).__init__()
        self.image = pg.image.load('material/images/Bullet_1.png').convert_alpha()
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.top = pea_rect.top
        self.rect.left = pea_rect.left + 10

        self.width = back_size[0]
        self.speed = 10
        self.attack = 1

    def update(self, *args):
        if self.rect.left < self.width:
            self.rect.left += self.speed
        else:
            self.kill()

