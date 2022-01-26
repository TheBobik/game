import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'data')
FPS = 60
score = 0
pygame.init()
screen = pygame.display.set_mode((480, 600))
pygame.display.set_caption("Набери 10 очков!")
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = path.join('data', name)
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = 240
        self.rect.bottom = 590
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > 480:
            self.rect.right = 480
        if self.rect.left < 0:
            self.rect.left = 0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(440)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)


background = load_image("starfield.png")
background_rect = background.get_rect()
player_img = load_image("car.png")
meteor_img = load_image("almaz1.png")
bullet_img = load_image("laserRed16.png")

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(15):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        for i in hits:
            i.kill()
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        score += 1
        print(score)
        if score >= 10:
            print('ПОБЕДА!')
            running = False
            exit()
    screen.fill((0, 0, 0))
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
