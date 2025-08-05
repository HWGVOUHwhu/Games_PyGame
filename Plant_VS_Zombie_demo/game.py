import time
import pygame as pg
import os
from Peashooter import Peashooter
from Sunflower import Sunflower
from WallNut import WallNut
from Sun import Sun
from Zombie import Zombie
from FlagZombie import FlagZombie
from Bullet import Bullet


pg.init()
pg.mixer.init()
back_size = (1200, 720)
FPS = 15
screen = pg.display.set_mode(back_size)
pg.display.set_caption('PVZ')
clock = pg.time.Clock()

back_path = 'material/images/background1.jpg'
back_obj = pg.image.load(back_path).convert_alpha()
pg.mixer.music.load('material/music/18 - Crazy Dave IN-GAME.mp3')

# sunbank_path = 'material/images/SunBack.png'
# sunbank_obj = pg.image.load(sunbank_path).convert_alpha()
seed_bank = pg.image.load('material/images/SeedBank.png').convert_alpha()
sunflower_seed = pg.image.load('material/images/Sunflower.gif').convert_alpha()
peashooter_seed = pg.image.load('material/images/Peashooter.gif').convert_alpha()
wallnut_seed = pg.image.load('material/images/WallNut.gif').convert_alpha()

sunflower_image = pg.image.load('material/images/SunFlower_00.png').convert_alpha()
peashooter_image = pg.image.load('material/images/Peashooter_00.png').convert_alpha()
wallnut_image = pg.image.load('material/images/WallNut_00.png').convert_alpha()
# peashooter = Peashooter()
# sunflower = Sunflower()
# wallnut = WallNut()
# zombie = Zombie()

# sun_list = []

# sprite_group = pg.sprite.Group()
# spirit_group.add(peashooter)
# spirit_group.add(sunflower)
# spirit_group.add(wallnut)
# sprite_group.add(zombie)

plant_group = pg.sprite.Group()
zombie_group = pg.sprite.Group()
sun_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()

sun_num = 500
sun_font = pg.font.SysFont('arial', 25)
sun_num_surface = sun_font.render(f'{sun_num}', True, (0, 0, 0))

GEN_SUN_EVENT = pg.USEREVENT + 1
pg.time.set_timer(GEN_SUN_EVENT, 1000)

GEN_BULLET_EVENT = pg.USEREVENT + 2
pg.time.set_timer(GEN_BULLET_EVENT, 2500)

GEN_ZOMBIE_EVENT = pg.USEREVENT + 3
pg.time.set_timer(GEN_ZOMBIE_EVENT, 10000)

GEN_FLAGZOMBIE_EVENT = pg.USEREVENT + 4
pg.time.set_timer(GEN_FLAGZOMBIE_EVENT, 20000)


def main():
    global sun_num, sun_num_surface
    running = True
    index = 0
    choose = 0
    if not pg.mixer.get_busy():
        pg.mixer.music.play()

    while running:

        # 界面维护
        if index >= 1300:
            index = 0

        clock.tick(FPS)
        screen.blit(back_obj, (0, 0))
        screen.blit(seed_bank, (350, 0))
        screen.blit(sunflower_seed, (430, 10))
        screen.blit(peashooter_seed, (480, 10))
        screen.blit(wallnut_seed, (530, 10))
        screen.blit(sun_num_surface, (375, 57))

        (x, y) = pg.mouse.get_pos()
        if choose == 1:
            screen.blit(sunflower_image, (x, y))
        elif choose == 2:
            screen.blit(peashooter_image, (x, y))
        elif choose == 3:
            screen.blit(wallnut_image, (x, y))
        else:
            pass

        # 碰撞检测
        for bullet in bullet_group:
            for zombie in zombie_group:
                if pg.sprite.collide_mask(bullet, zombie):
                    bullet_group.remove(bullet)
                    bullet.kill()
                    zombie.energy -= bullet.attack

        for plant in plant_group:
            for zombie in zombie_group:
                if pg.sprite.collide_mask(plant, zombie):
                    plant.zombies.add(zombie)
                    zombie.is_eating = True

        # 操作执行
        for event in pg.event.get():
            if event.type == GEN_SUN_EVENT:
                for plant in plant_group:
                    if isinstance(plant, Sunflower):
                        now = time.time()
                        if now - plant.last_time >= 10:
                            sun = Sun(plant.rect)
                            sun_group.add(sun)
                            plant.last_time = now
            if event.type == GEN_BULLET_EVENT:
                for plant in plant_group:
                    if isinstance(plant, Peashooter):
                        now = time.time()
                        if now - plant.last_time >= 2:
                            bullet = Bullet(plant.rect, back_size)
                            bullet_group.add(bullet)
                            plant.last_time = now
            if event.type == GEN_ZOMBIE_EVENT:
                zombie = Zombie()
                zombie_group.add(zombie)
            if event.type == GEN_FLAGZOMBIE_EVENT:
                flag_zombie = FlagZombie()
                zombie_group.add(flag_zombie)
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pressed_key = pg.mouse.get_pressed()
                if pressed_key[0]:
                    pos = pg.mouse.get_pos()
                    x, y = pos
                    if 430 <= x <= 480 and 10 <= y <= 80 and sun_num >= 50:
                        print("SunFlower")
                        if choose != 1:
                            choose = 1
                        else:
                            choose = 0
                    elif 480 < x <= 530 and 10 <= y <= 80 and sun_num >= 100:
                        print("Peashooter")
                        if choose != 2:
                            choose = 2
                        else:
                            choose = 0
                    elif 530 < x <= 580 and 10 <= y <= 80 and sun_num >= 50:
                        print("WallNut")
                        if choose != 3:
                            choose = 3
                        else:
                            choose = 0
                    elif 250 < x < 1200 and 87 < y < 720 and choose != 0:
                        print((x, y))
                        if choose == 1:
                            current_time = time.time()
                            sunflower = Sunflower(current_time)
                            sunflower.rect.top = y
                            sunflower.rect.left = x
                            plant_group.add(sunflower)
                            sun_num -= 50
                        elif choose == 2:
                            current_time = time.time()
                            peashooter = Peashooter(current_time)
                            peashooter.rect.top = y
                            peashooter.rect.left = x
                            plant_group.add(peashooter)
                            sun_num -= 100
                        elif choose == 3:
                            wallnut = WallNut()
                            wallnut.rect.top = y
                            wallnut.rect.left = x
                            plant_group.add(wallnut)
                            sun_num -= 50
                        sun_num_surface = sun_font.render(f'{sun_num}', True, (0, 0, 0))
                        choose = 0
                    else:
                        pass
                    for sun in sun_group:
                        if sun.rect.collidepoint(pos):
                            sun_group.remove(sun)
                            sun.kill()
                            sun_num += 50
                            sun_num_surface = sun_font.render(f'{sun_num}', True, (0, 0, 0))

        # 对象更新
        plant_group.update(index)
        zombie_group.update(index)
        sun_group.update(index)
        bullet_group.update(index)

        plant_group.draw(screen)
        zombie_group.draw(screen)
        sun_group.draw(screen)
        bullet_group.draw(screen)

        pg.display.update()

        index += 1


if __name__ == '__main__':
    main()
