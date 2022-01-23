import pygame
import os
import sys


def load_image(name, color_key=None):
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
    return image


pygame.init()
FPS = 50
size = 850
screen_size = (size, size)
screen = pygame.display.set_mode(screen_size)

tile_images = {
    'rocket': load_image('rocket.png'),
    'cave': load_image('cave.png'),
    'oxygen': load_image('O2.png'),
    'black': load_image('black.png'),
    'oxygent': load_image('oxygent.png'),
    'empty1': load_image('moon1.png'),
    'empty2': load_image('moon2.png'),
    'empty3': load_image('invisible.png'),
    'nooxygent': load_image('nooxygent.png')
}
player_image = load_image('astronaut.png')
bg = load_image('space.jpg')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def TitleOx(full):
    image = load_image('nooxygent.png')
    for i in range(full):
        screen.blit(image, (i * 0.5, 0))
    for y in range(full, 10):
        screen.blit(image, (y * 0.5, 0))


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


oxy = 1000
player = None
ready = False
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
            elif level[y][x] == '1':
                Tile('black', x, y)
            elif level[y][x] == '@':
                Tile('empty1', x, y)
                new_player = Player(x, y)
    return new_player, x, y


def move(hero, movement):
    global ready
    if oxy > 0:
        x, y = hero.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] == "." or level_map[y - 1][x] == "@" \
                    or level_map[y - 1][x] == "," or level_map[y - 1][x] == "0" or level_map[y - 1][x] == "#":
                if level_map[y - 1][x] == "." or level_map[y - 1][x] == ",":
                    oxygen('minus')
                elif level_map[y - 1][x] == "0":
                    oxygen('full')
                    Tile('empty1', x, y - 1)
                if level_map[y - 1][x] == "#":
                    ready = True
                else:
                    ready = False
                hero.move(x, y - 1)
        elif movement == "down":
            if y < max_y and level_map[y + 1][x] == "." or level_map[y + 1][x] == "@" \
                    or level_map[y + 1][x] == "," or level_map[y + 1][x] == "0" or level_map[y + 1][x] == "#":
                if level_map[y + 1][x] == "." or level_map[y + 1][x] == ",":
                    oxygen('minus')
                elif level_map[y + 1][x] == "0":
                    oxygen('full')
                    Tile('empty1', x, y + 1)
                if level_map[y + 1][x] == "#":
                    ready = True
                else:
                    ready = False
                hero.move(x, y + 1)
        elif movement == "left":
            if x > 0 and level_map[y][x - 1] == "." or level_map[y][x - 1] == "@" \
                    or level_map[y][x - 1] == "," or level_map[y][x - 1] == "0" or level_map[y][x - 1] == "#":
                if level_map[y][x - 1] == "." or level_map[y][x - 1] == ",":
                    oxygen('minus')
                elif level_map[y][x - 1] == "0":
                    oxygen('full')
                    Tile('empty1', x - 1, y)
                if level_map[y][x - 1] == "#":
                    ready = True
                else:
                    ready = False
                hero.move(x - 1, y)
        elif movement == "right":
            if x < max_x and level_map[y][x + 1] == "." or level_map[y][x + 1] == "@" \
                    or level_map[y][x + 1] == "," or level_map[y][x + 1] == "0" or level_map[y][x + 1] == "#":
                if level_map[y][x + 1] == "." or level_map[y][x + 1] == ",":
                    oxygen('minus')
                elif level_map[y][x + 1] == "0":
                    oxygen('full')
                    Tile('empty1', x + 1, y)
                if level_map[y][x + 1] == "#":
                    ready = True
                else:
                    ready = False
                hero.move(x + 1, y)


def oxygen(status):
    global oxy
    if oxy > 0:
        if status == 'minus':
            oxy -= 10
        elif status == 'full':
            oxy = 100
    print(oxy)


def message(msg, k):
    x, y = screen_size
    text_style = pygame.font.SysFont("bahnschrift", 25)
    mesg = text_style.render(msg, True, (155, 0, 0))
    screen.blit(mesg, (x // 2.5 - 5 ** k, y // 3 + 35 * k))


def show_menu():
    pass


def terminate():
    pygame.quit()
    quit()


camera = Camera()
level_map = load_level('map.txt')
hero, max_x, max_y = generate_level(level_map)
camera.update(hero)


def gameloop():
    global oxy

    while oxy == 0:
        message('Вы проиграли!', 2)
        message('Нажмите "Q" чтобы выйти из игры', 3)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    terminate()
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
                        os.system('python minigame.py')
                        print('press')
        screen.fill(pygame.Color("black"))
        screen.blit(bg, (0, 0))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        if ready:
            message('Нажмите "Y" для начала мини игры', 1)
            pygame.display.flip()
        pygame.display.flip()
        if oxy == 0:
            gameloop()
    terminate()


gameloop()
