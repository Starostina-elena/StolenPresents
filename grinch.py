import os
import sys
import random
import time

import pygame

flag = True
pygame.display.set_caption('Present for Grinch')
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

FPS = 50

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Пройдите к сундуку!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (500, 500))
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = [pos_x, pos_y]
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(
            tile_width * x + 15, tile_height * y + 5)
        self.pos = [x, y]

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '^':
                Tile('chest', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

def message(msg, color):
    font_style = pygame.font.SysFont("arial", 25)
    mess = font_style.render(msg, True, color)
    present = pygame.transform.scale(load_image('present.png'), (100, 100))
    rect = present.get_rect(
        bottomright=(100, 100))
    screen.blit(present, rect)
    screen.blit(mess, [30, 225])

def move(hero, movement):
    global level_x, level_y, flag
    x, y = hero.pos
    if x == 7 and y == 8:
        flag = False
    if flag:
        if movement == "up":
            if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] == "@" or level_map[y - 1][x] == "^"):
                hero.move(x, y - 1)
        elif movement == "down":
            if y < level_y - 1 and (
                    level_map[y + 1][x] == "." or level_map[y + 1][x] == "@" or level_map[y + 1][x] == "^"):
                hero.move(x, y + 1)
        elif movement == "left":
            if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] == "@" or level_map[y][x - 1] == "^"):
                hero.move(x - 1, y)
        elif movement == "right":
            if x < level_x - 1 and (
                    level_map[y][x + 1] == "." or level_map[y][x + 1] == "@" or level_map[y][x + 1] == "^"):
                hero.move(x + 1, y)
    else:
        screen.fill('white')
        message("Поздравляем! Вы нашли подарок для Гринча!", "red")
        pygame.display.update()
        time.sleep(4)
        exit()


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('stenka.png'),
    'empty': load_image('pol1.png'),
    'chest': load_image('finalc.png')
}
player_image = load_image('dedmoroz.png')

tile_width = tile_height = 50

clock = pygame.time.Clock()
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
start_screen()
level_map = load_level('map.txt')
player, level_x, level_y = generate_level(load_level('map.txt'))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if key[pygame.K_DOWN]:
            move(player, 'down')
        if key[pygame.K_UP]:
            move(player, 'up')
        if key[pygame.K_LEFT]:
            move(player, 'left')
        if key[pygame.K_RIGHT]:
            move(player, 'right')


    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
