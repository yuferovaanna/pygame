import os
import pygame
import sys
from random import randrange, choice

pygame.init()
pygame.key.set_repeat(200, 70)

running = True

FPS = 60
WIDTH = 720
HEIGHT = 900
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
player_sprites = pygame.sprite.Group()
ufo_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


# загрузка изображений
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('DESDEMONA', 100)
    text_coord = HEIGHT // 2 + 200
    string_rendered = font.render("PLAY", 4, pygame.Color('#DAA520'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = WIDTH // 2 - 75
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# противники и их генерация
class Ufo(pygame.sprite.Sprite):
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = load_image(choice(["ufo1.png", "ufo2.png",
                                        "ufo3.png", "ufo4.png"]))
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = randrange(50, 620)
        self.rect.y = -10

    def update(self):
        self.rect = self.rect.move(randrange(3) - 1,
                                   randrange(3) - 1)

    def update(self):
        self.rect.y += 1

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def kill(self):
        pygame.sprite.Sprite.kill(self)


# игрок и его генерация
class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = Player.image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 50

    def right(self):
        if self.rect.x < 620:
            self.rect.x += 15

    def left(self):
        if self.rect.x > 50:
            self.rect.x -= 15

    def get_cordinate(self):
        return self.rect.x, self.rect.y

    def new_game(self):
        self.rect.x = WIDTH // 2
        self.rect.y = HEIGHT - 50


# снаряд
class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = load_image("bullet.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 2

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def kill(self):
        pygame.sprite.Sprite.kill(self)


# картинка Game over
class GameOver(pygame.sprite.Sprite):
    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(group)
        self.image = load_image("gameover.png")
        self.image = pygame.transform.scale(self.image, (720, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT // 3 + 100

    def new_game(self):
        pygame.sprite.Sprite.kill(self)


start_screen()
create_timer = pygame.time.get_ticks()
player = Player(player_sprites)
count = 0


# record = 0


def tick_logic():
    if count % 70 == 0:
        Ufo(ufo_sprites)
    for ufo in ufo_sprites:
        ufo.update()
        if ufo.get_y() == 850:
            GameOver(player_sprites)
            ufo.kill()
        for bullet in bullet_sprites:
            bullet.update()
            num = ufo.get_y()
            num1 = ufo.get_x()
            if bullet.get_y() == -10:
                bullet.kill()
            if bullet.get_y() in range(num - 10, num + 50) and\
                    bullet.get_x() in range(num1 - 10, num1 + 50):
                bullet.kill()
                ufo.kill()


# перезагрузка игры
def game_over():
    for player in player_sprites:
        player.new_game()
    for ufo in ufo_sprites:
        ufo.kill()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for left in player_sprites:
                    left.left()
            elif event.key == pygame.K_RIGHT:
                for right in player_sprites:
                    right.right()
            elif event.key == pygame.K_q:
                x, y = player.get_cordinate()
                Bullet(bullet_sprites, x, y)
            elif event.key == pygame.K_r:
                game_over()
    tick_logic()
    count += 1

    screen.fill(pygame.Color(0, 0, 0))
    ufo_sprites.draw(screen)
    player_sprites.draw(screen)
    bullet_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

terminate()
