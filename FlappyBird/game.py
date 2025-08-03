import pygame as pg
import random, os, sys
from sprites.Bird import Bird
from sprites.Pipe import Pipe


BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Constants
W, H = 288, 512
FPS = 30

# Setup
pg.init()
SCREEN = pg.display.set_mode((W, H))
CLOCK = pg.time.Clock()
pg.display.set_caption('Flappy_Bird')
icon = pg.image.load('assets/sprites/red-mid.png')
icon = pg.transform.scale(icon, (24, 24))
pg.display.set_icon(icon)

# Materials
IMAGES = {}
for image in os.listdir('assets/sprites'):
    name, _ = os.path.splitext(image)
    path = os.path.join('assets/sprites', image)
    IMAGES[name] = pg.image.load(path)

FLOOR_Y = H - IMAGES['floor'].get_height()

# Music
AUDIO = {}
for audio in os.listdir('assets/audio'):
    name, _ = os.path.splitext(audio)
    path = os.path.join('assets/audio', audio)
    AUDIO[name] = pg.mixer.Sound(path)


def show_score(score):
    score_str = str(int(score))
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w


def menu_window():
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0

    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (FLOOR_Y - IMAGES['guide'].get_height()) / 2

    bird_x = W * 0.2
    bird_y = (H - IMAGES['birds'][0].get_height()) / 2
    bird_y_vel = 1
    bird_y_range = [bird_y - 8, bird_y + 8]

    idx = 0
    repeat = 3
    frames = [0] * repeat + [1] * repeat + [2] * repeat + [1] * repeat

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                return

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        bird_y += bird_y_vel
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]:
            bird_y_vel *= -1

        idx = (idx + 1) % len(frames)

        SCREEN.blit(IMAGES['back'], (0, 0))
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        SCREEN.blit(IMAGES['guide'], (guide_x, guide_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x, bird_y))
        pg.display.update()
        CLOCK.tick(FPS)


def game_window():
    AUDIO['flap'].play()
    floor_gap = IMAGES['floor'].get_width() - W
    floor_x = 0

    bird = Bird(W * 0.2, H * 0.4, IMAGES['birds'], FLOOR_Y)

    distance = 150
    pipe_gap = 100
    n = 4
    pipes_group = pg.sprite.Group()

    score = 0

    for i in range(n):
        pipe_y = random.randint(int(H*0.3), int(H*0.7))
        pipe_up = Pipe(W+i*distance, pipe_y, IMAGES['pipes'], True)
        pipe_down = Pipe(W + i * distance, pipe_y-pipe_gap, IMAGES['pipes'], False)
        pipes_group.add(pipe_up)
        pipes_group.add(pipe_down)

    while True:
        flap = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                flap = True
                AUDIO['flap'].play()

        floor_x -= 4
        if floor_x <= -floor_gap:
            floor_x = 0

        SCREEN.blit(IMAGES['back'], (0, 0))
        pipes_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (floor_x, FLOOR_Y))
        SCREEN.blit(bird.image, bird.rect)

        bird.update(flap)

        first_pipe_up = pipes_group.sprites()[0]
        first_pipe_down = pipes_group.sprites()[1]
        if first_pipe_up.rect.right < 0:
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n * distance, pipe_y, IMAGES['pipes'], True)
            new_pipe_down = Pipe(first_pipe_down.rect.x + n * distance, pipe_y-pipe_gap, IMAGES['pipes'], False)
            pipes_group.add(new_pipe_up)
            pipes_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()

        pipes_group.update()

        if bird.rect.y > FLOOR_Y or bird.rect.y < 0 or pg.sprite.spritecollideany(bird, pipes_group):
            AUDIO['hit'].play()
            AUDIO['die'].play()
            result = {'bird': bird, 'pipes': pipes_group, 'score': score}
            bird.died = True
            return result

        # if bird.rect.left + 2*first_pipe_up.x_vel < first_pipe_up.rect.centerx < bird.rect.left:
        #     AUDIO['score'].play()
        #     score += 1
        for pipe in pipes_group:
            if bird.rect.left > pipe.rect.centerx and not pipe.scored and pipe.upwards:
                AUDIO['score'].play()
                score += 1
                pipe.scored = True

        show_score(score)

        pg.display.update()
        CLOCK.tick(FPS)


def end_window(result):

    gameover_x = (W - IMAGES['gameover'].get_width()) / 2
    gameover_y = (FLOOR_Y - IMAGES['gameover'].get_height()) / 2

    bird = result['bird']

    while True:
        if bird.died:
            bird.go_die()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    return

        SCREEN.blit(IMAGES['back'], (0, 0))
        result['pipes'].draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, FLOOR_Y))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        SCREEN.blit(bird.image, bird.rect)
        show_score(result['score'])
        pg.display.update()
        CLOCK.tick(FPS)


def main():
    while True:
        AUDIO['start'].play()
        IMAGES['back'] = IMAGES[random.choice(['day', 'night'])]
        color = random.choice(['red', 'yellow', 'blue'])
        IMAGES['birds'] = [IMAGES[color+'-up'], IMAGES[color+'-mid'], IMAGES[color+'-down']]
        pipe = IMAGES[random.choice(['green-pipe', 'red-pipe'])]
        IMAGES['pipes'] = [pipe, pg.transform.flip(pipe, False, True)]
        menu_window()
        result = game_window()
        end_window(result)


if __name__ == '__main__':
    main()
