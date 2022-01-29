import pygame
import os
import random
import sys


def load_image(name, color_key=None, transform=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    if transform:
        image = pygame.transform.scale(image, (40, 40))
    return image


pygame.init()
FPS = 50
size = 850
oxy = 100
player = None
ready = False
rocket_ready = False
rocket_parts = 0
scr = 0
map_id = 0
name_player = ''
screen_size = (size, size)
screen = pygame.display.set_mode(screen_size)

tile_images = {
    'rocket': load_image('broken_rocket.png'),
    'cave': load_image('cave.png'),
    'oxygen': load_image('O2.png'),
    'empty1': load_image('moon1.png'),
    'empty2': load_image('moon2.png'),
    'empty3': load_image('invisible.png')
}
player_image = load_image('astronaut.png')
peace_of_rocket = load_image('peace_of_rocket.png')
o2 = load_image('draw_o2.png')
bg = load_image('space.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx += tile_width * (x - self.pos[0])
        camera.dy += tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] - self.dx
        obj.rect.y = obj.abs_pos[1] - self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty1', x, y)
            elif level[y][x] == ',':
                Tile('empty2', x, y)
            elif level[y][x] == '!':
                Tile('rocket', x, y)
            elif level[y][x] == '0':
                Tile('oxygen', x, y)
            elif level[y][x] == '#':
                Tile('cave', x, y)
            elif level[y][x] == '@':
                Tile('empty1', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move(hero, movement):
    global ready, rocket_ready
    if oxy > 0:
        x, y = hero.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] != "`":
                if level_map[y - 1][x] == "." or level_map[y - 1][x] == "," or level_map[y - 1][x] == "@":
                    oxygen('minus')
                    score('step')
                elif level_map[y - 1][x] == "0":
                    oxygen('full')
                    score('fullo')
                    Tile('empty1', x, y - 1)
                if level_map[y - 1][x] == "#":
                    ready = True
                else:
                    ready = False
                if level_map[y - 1][x] == "!":
                    if rocket_parts == 1:
                        rocket_ready = True
                hero.move(x, y - 1)

        elif movement == "down":
            if y < max_y and level_map[y + 1][x] != "`":
                if level_map[y + 1][x] == "." or level_map[y + 1][x] == "," or level_map[y + 1][x] == "@":
                    oxygen('minus')
                    score('step')
                elif level_map[y + 1][x] == "0":
                    oxygen('full')
                    score('fullo')
                    Tile('empty1', x, y + 1)
                if level_map[y + 1][x] == "#":
                    ready = True
                else:
                    ready = False
                if level_map[y + 1][x] == "!":
                    if rocket_parts == 1:
                        rocket_ready = True
                hero.move(x, y + 1)

        elif movement == "left":
            if x > 0 and level_map[y][x - 1] != "`":
                if level_map[y][x - 1] == "." or level_map[y][x - 1] == "," or level_map[y][x - 1] == "@":
                    oxygen('minus')
                    score('step')
                elif level_map[y][x - 1] == "0":
                    oxygen('full')
                    score('fullo')
                    Tile('empty1', x - 1, y)
                if level_map[y][x - 1] == "#":
                    ready = True
                else:
                    ready = False
                if level_map[y][x - 1] == "!":
                    if rocket_parts == 1:
                        rocket_ready = True
                hero.move(x - 1, y)

        elif movement == "right":
            if x < max_x and level_map[y][x + 1] != "`":
                if level_map[y][x + 1] == "." or level_map[y][x + 1] == "," or level_map[y][x + 1] == "@":
                    oxygen('minus')
                    score('step')
                elif level_map[y][x + 1] == "0":
                    oxygen('full')
                    score('fullo')
                    Tile('empty1', x + 1, y)
                if level_map[y][x + 1] == "#":
                    ready = True
                else:
                    ready = False
                if level_map[y][x + 1] == "!":
                    if rocket_parts == 1:
                        rocket_ready = True
                hero.move(x + 1, y)


def oxygen(status):
    global oxy
    if oxy > 0:
        if status == 'minus':
            oxy -= 10
        elif status == 'full':
            oxy = 100
    print(oxy)


def message(msg, k=1):
    style = pygame.font.SysFont("malgungothic", 25)
    mesg = style.render(msg, True, (155, 0, 0))
    screen.blit(mesg, (size // 2.5 - 5 ** k, size // 3 + 35 * k))


def score(status='draw'):
    global scr

    if status == 'step':
        scr += 10
    elif status == 'fullo':
        scr += 100
    elif status == 'rocketpart':
        scr += 1000
    if status == 'draw':
        pygame.draw.rect(screen, (128, 128, 128), (605, 0, 245, 55))
        pygame.draw.rect(screen, (255, 255, 255), (610, 5, 235, 45))
        style = pygame.font.SysFont("aesthetic", 35)
        text = style.render(f'Your score: {scr}', True, (128, 128, 128))
        screen.blit(text, (615, 17))


def start_screen():
    global map_id
    intro_text = 'Нажмите клавиши от 1 до 3 чтобы выбрать уровень!'

    fon = pygame.transform.scale(load_image('zastavka'), screen_size)
    screen.blit(fon, (0, 0))
    style = pygame.font.SysFont("aesthetic", 35)
    text = style.render(intro_text, True, (148, 0, 211))
    screen.blit(text, (125, 340))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    map_id = 1
                    return
                elif event.key == pygame.K_2:
                    map_id = 2
                    return
                elif event.key == pygame.K_3:
                    map_id = 3
                    return

        pygame.display.flip()
        clock.tick(FPS)


def end_screen():

    fon = pygame.transform.scale(load_image('end.png'), screen_size)
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                terminate()

        pygame.display.flip()
        clock.tick(FPS)


def score_consumables():
    pygame.draw.rect(screen, (128, 128, 128), (0, 0, 155, 55))
    pygame.draw.rect(screen, (255, 255, 255), (5, 5, 145, 45))
    screen.blit(o2, (6, 10))
    screen.blit(peace_of_rocket, (80, 11))
    style = pygame.font.SysFont("aesthetic", 35)
    text = style.render(f'{oxy // 10}', True, (128, 128, 128))
    text2 = style.render(f'{rocket_parts}/1', True, (128, 128, 128))
    screen.blit(text, (35, 17))
    screen.blit(text2, (105, 17))


def terminate():
    pygame.quit()
    quit()


start_screen()
camera = Camera()
level_map = load_level(f'map{map_id}.txt')
hero, max_x, max_y = generate_level(level_map)
camera.update(hero)


def gameloop():
    global oxy, rocket_parts

    while oxy == 0:
        os.system('python end.py')

    while oxy != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move(hero, "up")
                elif event.key == pygame.K_DOWN:
                    move(hero, "down")
                elif event.key == pygame.K_LEFT:
                    move(hero, "left")
                elif event.key == pygame.K_RIGHT:
                    move(hero, "right")
                if ready:
                    if event.key == pygame.K_y:
                        '''вы действительнохотите начать игру?'''
                        os.system('python minigame.py')
                        score('rocketpart')
                        rocket_parts += 1
                        print(rocket_parts)
        screen.blit(bg, (0, 0))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        score()
        score_consumables()
        clock.tick(FPS)

        if ready:
            message('Нажмите "Y" для начала мини игры', 1)
            pygame.display.flip()

        if rocket_ready:
            message('Нажмите "Y" чтобы попробывать восстановить ракету!', 1)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        print(1)
                        end_screen()

        pygame.display.flip()

        if oxy == 0:
            gameloop()

    terminate()


gameloop()
