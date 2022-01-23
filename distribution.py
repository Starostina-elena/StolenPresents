import os
import sys
import time

import pygame


def load_image(name, colorkey=0, transform=None):
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
    if transform:
        image = pygame.transform.scale(image, (40, 40))
    return image


def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["Пройдите к деревню!"]

    fon = pygame.transform.scale(load_image('country.png'), (550, 550))
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

def animation():
    global animation_n
    global animation_i
    animation_n += 1
    if animation_n % 5 == 0:
        animation_i = (animation_i + 1) % 8
        player.change_picture(animation_i)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = [pos_x, pos_y]
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 5)

    def move(self, x, y):
        self.rect = self.image.get_rect().move(
            tile_width * x + 10, tile_height * y + 5)
        self.pos = [x, y]

    def change_picture(self, n):
        self.image = animation_set[n]

def generate_level(level):
    global a
    new_player, x, y = None, None, None
    counter_of_houses = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                counter_of_houses += 1
                if counter_of_houses <= a:
                    Tile('chest', x, y)
                else:
                    Tile('empty', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y

def message(msg, color):
    font_style = pygame.font.SysFont("arial", 25)
    mess = font_style.render(msg, True, color)
    present = pygame.transform.scale(load_image('present.png'), (100, 100))
    rect = present.get_rect(
        bottomright=(325, 400))
    screen.blit(present, rect)
    screen.blit(mess, [30, 225])

def show_message(message, font_size=50):
    global width, screen
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(message, True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
    present = pygame.transform.scale(load_image('present.png'), (200, 200))
    rect = present.get_rect(
        bottomright=(350, 300))
    screen.blit(present, rect)
    screen.blit(string_rendered, intro_rect)

def move(hero, movement):
    global level_x, level_y, flag, a, x_position, y_position, a, houses, houses_coordinars
    x, y = hero.pos
    if flag:
        if movement == "up":
            if y > 0 and (level_map[y - 1][x] == "." or level_map[y - 1][x] == "@"):
                hero.move(x, y - 1)
                if houses != 1:
                    if [x, y - 1] in houses_coordinars:
                        houses -= 1
                        screen.fill('white')
                        pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
                        if houses == 1:
                            show_message(f"Остался {houses} подарок")
                        elif houses == 2 or houses == 3 or houses == 4:
                            show_message(f"Осталось {houses} подарка")
                        elif houses == 5 or houses == 6 or houses == 7:
                            show_message(f"Осталось {houses} подарков")
                        pygame.display.update()
                        time.sleep(1)
                else:
                    flag = False
        elif movement == "down":
            if y < level_y - 1 and (
                    level_map[y + 1][x] == "." or level_map[y + 1][x] == "@"):
                hero.move(x, y + 1)
                if houses != 1:
                    if [x, y + 1] in houses_coordinars:
                        houses -= 1
                        screen.fill('white')
                        pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
                        if houses == 1:
                            show_message(f"Остался {houses} подарок")
                        elif houses == 2 or houses == 3 or houses == 4:
                            show_message(f"Осталось {houses} подарка")
                        elif houses == 5 or houses == 6 or houses == 7:
                            show_message(f"Осталось {houses} подарков")
                        pygame.display.update()
                        time.sleep(1)
                else:
                    flag = False
        elif movement == "left":
            if x > 0 and (level_map[y][x - 1] == "." or level_map[y][x - 1] == "@"):
                hero.move(x - 1, y)
                if houses != 1:
                    if [x - 1, y] in houses_coordinars:
                        houses -= 1
                        screen.fill('white')
                        pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
                        if houses == 1:
                            show_message(f"Остался {houses} подарок")
                        elif houses == 2 or houses == 3 or houses == 4:
                            show_message(f"Осталось {houses} подарка")
                        elif houses == 5 or houses == 6 or houses == 7:
                            show_message(f"Осталось {houses} подарков")
                        pygame.display.update()
                        time.sleep(1)
                else:
                    flag = False
        elif movement == "right":
            if x < level_x - 1 and (
                    level_map[y][x + 1] == "." or level_map[y][x + 1] == "@"):
                hero.move(x + 1, y)
                if houses != 1:
                    if [x + 1, y] in houses_coordinars:
                        houses -= 1
                        screen.fill('white')
                        pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
                        if houses == 1:
                            show_message(f"Остался {houses} подарок")
                        elif houses == 2 or houses == 3 or houses == 4:
                            show_message(f"Осталось {houses} подарка")
                        elif houses == 5 or houses == 6 or houses == 7:
                            show_message(f"Осталось {houses} подарков")
                        pygame.display.update()
                        time.sleep(1)
                else:
                    flag = False
    else:
        screen.fill('white')
        message("Поздравляем! Вы раздали подарки всем жителям!", "red")
        pygame.display.update()
        time.sleep(3)
        exit()


if __name__ == '__main__':
    photos = ['Дед мороз.png', 'Дед мороз(кадр2).png', 'Дед мороз(кадр3).png',
              'Дед мороз(кадр2).png', 'Дед мороз.png', 'Дед мороз(кадр4).png',
              'Дед мороз(кадр5).png', 'Дед мороз(кадр4).png']
    animation_set = [load_image(i, transform=True) for i in photos]
    animation_n = 0
    animation_i = 0
    player_image = animation_set[animation_i]
    flag = True
    a = int(input())  # количество подарков
    houses = a
    pygame.display.set_caption('Present for people')
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    my = []
    if a == 1:
        houses_coordinars = [[2, 3]]
    elif a == 2:
        houses_coordinars = [[2, 3], [2, 5]]
    elif a == 3:
        houses_coordinars = [[2, 3], [2, 7], [2, 5]]
    elif a == 4:
        houses_coordinars = [[2, 3], [8, 2], [2, 7], [2, 5]]
    elif a == 5:
        houses_coordinars = [[2, 3], [8, 2], [8, 4], [2, 7], [2, 5]]
    elif a == 6:
        houses_coordinars = [[2, 3], [8, 2], [8, 4], [8, 6], [2, 7], [2, 5]]
    elif a == 7:
        houses_coordinars = [[2, 3], [8, 2], [8, 4], [8, 6], [8, 8], [2, 7], [2, 5]]
    FPS = 50
    x_position = 0
    y_position = 0

    player = None

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tile_images = {
        'wall': load_image('fffa.png'),
        'empty': load_image('sn.png'),
        'chest': load_image('h.png')
    }
    player_image = load_image('dedmoroz.png')

    tile_width = tile_height = 50

    clock = pygame.time.Clock()
    pygame.init()
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    start_screen()
    level_map = load_level('map1.txt')
    player, level_x, level_y = generate_level(load_level('map1.txt'))
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
