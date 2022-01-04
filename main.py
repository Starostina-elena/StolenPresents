import os
import sys

import pygame

FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Здесь",
                  "будет",
                  "анимация"]

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
        image = pygame.transform.scale(image, (45, 45))
    return image


def move(hero, movement):
    x, y = hero.pos
    global level_x
    global level_y

    # Я закомментила принты, тк они иногда ломают игру
    # print(level_map[x][y - 1])
    # print(level_map[x][y + 1])
    # print(level_map[x - 1][y])
    # print(level_map[x][y + 1])
    # print()

    # TODO: Может, не стоит оставлять вот эти ифы с or?
    # Просто если добавим потом еще какие то значки, придется усложнять or
    # Как вариант проверять что эта штука не равна решетке
    # Можно создать группу спрайтов со стенами и прочими препятствиями и
    # проверять что игрок не сталкивается ни с чем из этой группы при перемещении
    if movement == "up":
        hero.move((0, -0.05))
    elif movement == "down":
        hero.move((0, 0.05))
    elif movement == "left":
        hero.move((-0.05, 0))
    elif movement == "right":
        hero.move((0.05, 0))


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
            elif level[y][x] == '%':
                Tile('empty', x, y)
                level[y] = level[y][:x] + '#' + level[y][x + 1:]
            elif level[y][x] == '*':
                Tile('empty', x, y)
                AnimatedSprite('portal', load_image("portal.png", -1), 4, 1, x * tile_width, y * tile_height)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, level


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, type, sheet, columns, rows, x, y):
        if type == 'portal':
            super().__init__(all_sprites, portals)
        else:
            super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.iter = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        x, y = self.rect.x, self.rect.y
        self.iter = (self.iter + 1) % 10
        if self.iter == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

def animation():
    global animation_n
    global animation_i
    animation_n += 1
    if animation_n % 5 == 0:
        animation_i = (animation_i + 1) % 8
        player.change_picture(animation_i)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, wall_group)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = [pos_x, pos_y]
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, coords):
        self.rect.x += coords[0] * tile_width
        self.rect.y += coords[1] * tile_height
        self.pos[0] += coords[0]
        self.pos[1] += coords[1]
        for i in wall_group:
            if pygame.sprite.collide_mask(self, i):
                if coords[0] < 0:
                    self.rect.x -= coords[0] * tile_width * 2
                    self.pos[0] -= coords[0] * 2
                else:
                    self.rect.x -= coords[0] * tile_width
                    self.pos[0] -= coords[0]
                if coords[1] < 0:
                    self.rect.y -= coords[1] * tile_height * 2
                    self.pos[1] -= coords[1] * 2
                else:
                    self.rect.y -= coords[1] * tile_height
                    self.pos[1] -= coords[1]

    def change_picture(self, n):
        self.image = animation_set[n]

class Camera:

    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


if __name__ == '__main__':
    photos = ['Дед мороз.png', 'Дед мороз(кадр2).png', 'Дед мороз(кадр3).png',
              'Дед мороз(кадр2).png', 'Дед мороз.png', 'Дед мороз(кадр4).png',
              'Дед мороз(кадр5).png', 'Дед мороз(кадр4).png']
    animation_set = [load_image(i, transform=True) for i in photos]
    animation_n = 0
    animation_i = 0
    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    portals = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()

    tile_images = {
        'wall': load_image('walls.jpg'),
        'empty': load_image('floors.jpg')
    }
    player_image = animation_set[animation_i]

    tile_width = tile_height = 50

    pygame.init()
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('StolenPresents')

    clock = pygame.time.Clock()

    start_screen()

    player, level_x, level_y, level_map = \
        generate_level(load_level('map2.txt'))

    size = width, height = 11 * tile_width, 11 * tile_height
    screen = pygame.display.set_mode(size)

    camera = Camera()

    directions = {"right": False, "left": False, "up": False, "down": False}
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            key = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                animation()
                if event.key == pygame.K_RIGHT:
                    directions['right'] = True
                elif event.key == pygame.K_LEFT:
                    directions['left'] = True
                elif event.key == pygame.K_UP:
                    directions['up'] = True
                elif event.key == pygame.K_DOWN:
                    directions['down'] = True
            if event.type == pygame.KEYUP:
                animation()
                if event.key == pygame.K_RIGHT:
                    directions['right'] = False
                elif event.key == pygame.K_LEFT:
                    directions['left'] = False
                elif event.key == pygame.K_UP:
                    directions['up'] = False
                elif event.key == pygame.K_DOWN:
                    directions['down'] = False
        if directions['right']:
            animation()
            move(player, 'right')
        if directions['left']:
            animation()
            move(player, 'left')
        if directions['up']:
            animation()
            move(player, 'up')
        if directions['down']:
            animation()
            move(player, 'down')

        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 0, 0))

        portals.update()

        all_sprites.draw(screen)
        player_group.draw(screen)
        portals.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

