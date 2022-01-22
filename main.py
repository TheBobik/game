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
screen_size = (850, 850)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'rocket': load_image('rocket.png'),
    'cave': load_image('cave.png'),
    'oxygen': load_image('O2.png'),
    'empty1': load_image('moon.png'),
    'black': load_image('black.png'),
    'oxygent': load_image('oxygent.png'),
    'nooxygent': load_image('nooxygent.png'),
    'empty2': load_image('moon.png')
}
player_image = load_image('astronaut.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


def TitleOx(full):
    for i in range(full):
        Tile('oxygent', i * 0.5, 0)
    for y in range(full, 10):
        Tile('nooxygent', y * 0.5, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


oxy = 100
player = None
running = True
clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = [""]

    fon = pygame.transform.scale(load_image('zastavka'), (1000, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


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
            elif level[y][x] == '?':
                Tile('oxygent', x, y)
            elif level[y][x] == '@':
                Tile('empty1', x, y)
                new_player = Player(x, y)

    return new_player, x, y


def oxygen(status):
    global oxy
    if oxy > 0:
        if status == 'minus':
            oxy -= 10
        elif status == 'full':
            oxy = 100
    print(oxy)


def move(hero, movement):
    if oxy > 0:
        x, y = hero.pos
        if movement == "up":
            if y > 0 and level_map[y - 1][x] == "." or level_map[y - 1][x] == "@" or level_map[y - 1][x] == "0":
                if level_map[y - 1][x] == ".":
                    oxygen('minus')
                elif level_map[y - 1][x] == "0":
                    oxygen('full')
                    Tile('empty1', x, y - 1)
                hero.move(x, y - 1)
        elif movement == "down":
            if y < max_y and level_map[y + 1][x] == "." or level_map[y + 1][x] == "@" or level_map[y + 1][x] == "0":
                if level_map[y + 1][x] == ".":
                    oxygen('minus')
                elif level_map[y + 1][x] == "0":
                    oxygen('full')
                    Tile('empty1', x, y + 1)
                hero.move(x, y + 1)
        elif movement == "left":
            if x > 0 and level_map[y][x - 1] == "." or level_map[y][x - 1] == "@" or level_map[y][x - 1] == "0":
                if level_map[y][x - 1] == ".":
                    oxygen('minus')
                elif level_map[y][x - 1] == "0":
                    oxygen('full')
                    Tile('empty1', x - 1, y)
                hero.move(x - 1, y)
        elif movement == "right":
            if x < max_x and level_map[y][x + 1] == "." or level_map[y][x + 1] == "@" or level_map[y][x + 1] == "0":
                if level_map[y][x + 1] == ".":
                    oxygen('minus')
                elif level_map[y][x + 1] == "0":
                    oxygen('full')
                    Tile('empty1', x + 1, y)
                hero.move(x + 1, y)
        TitleOx(oxy // 10)


start_screen()
camera = Camera()
level_map = load_level('map.txt')
hero, max_x, max_y = generate_level(level_map)
camera.update(hero)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
