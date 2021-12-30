import os
import sys

import pygame

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (800, 600))
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
                return
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


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def move(hero, movement):
    x, y = hero.pos
    global level_x
    global level_y
    print(level_map[x][y - 1])
    print(level_map[x][y + 1])
    print(level_map[x - 1][y])
    print(level_map[x][y + 1])
    print()
    if movement == "up":
        if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] ==
                      "@"):
            hero.move(x, y - 1)
    elif movement == "down":
        if y < level_y - 1 and (level_map[y + 1][x] == "." or
                                level_map[y + 1][x] == "@"):
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] ==
                      "@"):
            hero.move(x - 1, y)
    elif movement == "right":
        if x < level_x - 1 and (level_map[y][x + 1] == "." or
                                level_map[y][x + 1] == "@"):
            hero.move(x + 1, y)


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
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
            tile_width * pos_x, tile_height * pos_y)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        self.pos = x, y


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('walls.jpg'),
    'empty': load_image('floors.jpg')
}
player_image = load_image('main hero.png')

tile_width = tile_height = 50
pygame.init()
size = width, height = 550, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen()
level_map = load_level('map2.txt')
player, level_x, level_y = \
    generate_level(load_level('map2.txt'))
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



