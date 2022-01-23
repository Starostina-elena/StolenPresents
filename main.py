import datetime
import os
import sys

import pygame
import pygame_gui

from random import shuffle

import tic_tac_toe_game
import three_in_row
import mini_game_2048
import sapper_game
import stroyka
import game_snake
import tetris
from database import add_to_database, show_highscores
import grinch
import distribution


def tic_tac_toe():

    """Игра крестики-нолики"""

    global width, height, screen, size, number_of_presents

    if tic_tac_toe_game.start():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def game_three_in_row():

    """Игра три в ряд"""

    global width, height, screen, size, number_of_presents

    if three_in_row.main():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def game_2048():

    """Игра 2048"""

    global width, height, screen, size, number_of_presents

    if mini_game_2048.main():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def saper():

    """Игра сапер"""

    global width, height, screen, size, number_of_presents

    if sapper_game.start():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def tower():

    """Игра башня"""

    global width, height, screen, size, number_of_presents

    if stroyka.main():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def snake():

    """Игра змейка"""

    global width, height, screen, size, number_of_presents

    if game_snake.main():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def mini_game_tetris():

    """Игра тетрис"""

    global width, height, screen, size, number_of_presents

    if tetris.main():
        number_of_presents += 1

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def present_for_grinch():

    """Бонусный уровень с подарком для Гринча"""

    global width, height, screen, size, number_of_presents

    grinch.main()

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def presents_for_citizens():

    """Раздача подарков жителям"""

    global width, height, screen, size, number_of_presents

    distribution.main(number_of_presents)

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)


def terminate():

    """Выход из игры"""

    pygame.quit()
    sys.exit()


def show_text_message(text, position, color='white', font_size=30):

    """Вывод на экран текстового сообщения"""

    if type(text) == str:
        text = [text]

    font = pygame.font.Font(None, font_size)
    text_coord = position[1]
    for line in text:
        string_rendered = font.render(line, 1, pygame.Color(color))
        intro_rect = string_rendered.get_rect()
        text_coord += font_size // 3
        intro_rect.top = text_coord
        intro_rect.x = position[0]
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def start_screen():

    """Стартовый экран, получение имени игрока"""

    fon = pygame.transform.scale(load_image('main_beginning_fon.jpg'), (800, 600))
    screen.blit(fon, (0, 0))

    intro_text = ["Придумайте имя! Когда будете",
                  "готовы, нажмите пробел или энтер"]
    show_text_message(intro_text, (100, 25))

    manager2 = pygame_gui.UIManager((width, height))

    player_name = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((100, 100), (350, 100)), manager=manager2
    )
    player_name.background_colour = pygame.Color((255, 255, 255))
    player_name.border_colour = pygame.Color((0, 255, 0))
    player_name.text_colour = pygame.Color((200, 50, 0))
    player_name.border_width = 5
    player_name.font.size = 30
    player_name.length_limit = 18
    player_name.rebuild()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key in [13, 32] and player_name.get_text():  # 32 - код пробела, 13 - enter
                    return player_name.get_text()
            manager2.process_events(event)

        manager2.update(60/1000)
        player_name.redraw()
        manager2.draw_ui(screen)

        pygame.display.flip()
        clock.tick(FPS)


def show_history():

    """Показывает слайд-шоу, рассказывающее историю игры"""

    screen.fill((0, 0, 0))

    text = ['Гринч всегда ненавидел Новый год,',
            'и поэтому он решил испортить',
            'праздник',
            '']
    text2 = ['(нажмите любую кнопку, чтобы продолжить)']
    show_text_message(text, (25, 100), font_size=40)
    show_text_message(text2, (50, 300))

    slide = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                slide += 1
                if slide == 1:
                    screen.fill((255, 255, 255))
                    image = pygame.transform.scale(load_image('main_beginning_pic_1.jpg'), (550, 550))
                    image.set_colorkey(image.get_at((5, 60)))
                    screen.blit(image, (0, 0))
                elif slide == 2:
                    image = pygame.transform.scale(load_image('main_beginning_pic_2.jpg'), (1100, 550))
                    screen.blit(image, (-400, 0))
                elif slide == 3:
                    text = [
                        'Гринч украл Деда Мороза',
                        'и все его подарки...'
                    ]
                    show_text_message(text, (50, 200), font_size=40)
                elif slide == 4:
                    image = pygame.transform.scale(load_image('main_beginning_pic_3.jpg'), (700, 550))
                    screen.blit(image, (-75, 0))
                elif slide == 5:
                    text = [
                        'Теперь Дед Мороз заперт в',
                        'подземелье Гринча.',
                        'Помогите ему найти все подарки',
                        'и сбежать!'
                    ]
                    show_text_message(text, (35, 10), color=(150, 205, 150), font_size=40)
                else:
                    return

        pygame.display.flip()


def load_level(filename):

    """Чтение карты уровня из файла"""

    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=0, transform=None):

    """Загрузка изображения"""

    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if transform:
        image = pygame.transform.scale(image, (40, 40))
    return image


def prepare_movement():

    """Обрабатывает словарь directions для движения игрока"""

    global player_stands_on_portal, confirmation_mini_game_dialog

    if directions['right']:
        # Анимация Деда Мороза
        animation()
        # Передвижение (сообщение для подтверждения входа в мини-игру не надо создавать,
        # если оно уже есть (player_stands_on_portal) или если игрок не стоит на портале)
        if not pygame.sprite.spritecollideany(player,
                                              portals) or player_stands_on_portal:
            move(player, 'right')
            if not pygame.sprite.spritecollideany(player, portals):  # Удаление подтверждения входа в мини-игру
                # (если игрок сошел с портала)
                player_stands_on_portal = False
                if confirmation_mini_game_dialog is not None:
                    confirmation_mini_game_dialog.kill()
                    confirmation_mini_game_dialog = None
        else:
            # Создание сообщения для подтверждения входа в мини-игру
            create_confirmation_mini_game_dialog()
    if directions['left']:
        # Анимация Деда Мороза
        animation()
        # Передвижение (сообщение для подтверждения входа в мини-игру не надо создавать,
        # если оно уже есть (player_stands_on_portal) или если игрок не стоит на портале)
        if not pygame.sprite.spritecollideany(player,
                                              portals) or player_stands_on_portal:
            move(player, 'left')
            if not pygame.sprite.spritecollideany(player, portals):  # Удаление подтверждения входа в мини-игру
                # (если игрок сошел с портала)
                player_stands_on_portal = False
                if confirmation_mini_game_dialog is not None:
                    confirmation_mini_game_dialog.kill()
                    confirmation_mini_game_dialog = None
        else:
            # Создание сообщения для подтверждения входа в мини-игру
            create_confirmation_mini_game_dialog()
    if directions['up']:
        # Анимация Деда Мороза
        animation()
        # Передвижение (сообщение для подтверждения входа в мини-игру не надо создавать,
        # если оно уже есть (player_stands_on_portal) или если игрок не стоит на портале)
        if not pygame.sprite.spritecollideany(player,
                                              portals) or player_stands_on_portal:
            move(player, 'up')
            if not pygame.sprite.spritecollideany(player, portals):  # Удаление подтверждения входа в мини-игру
                # (если игрок сошел с портала)
                player_stands_on_portal = False
                if confirmation_mini_game_dialog is not None:
                    confirmation_mini_game_dialog.kill()
                    confirmation_mini_game_dialog = None
        else:
            # Создание сообщения для подтверждения входа в мини-игру
            create_confirmation_mini_game_dialog()
    if directions['down']:
        # Анимация Деда Мороза
        animation()
        # Передвижение (сообщение для подтверждения входа в мини-игру не надо создавать,
        # если оно уже есть (player_stands_on_portal) или если игрок не стоит на портале)
        if not pygame.sprite.spritecollideany(player,
                                              portals) or player_stands_on_portal:
            move(player, 'down')
            if not pygame.sprite.spritecollideany(player, portals):  # Удаление подтверждения входа в мини-игру
                # (если игрок сошел с портала)
                player_stands_on_portal = False
                if confirmation_mini_game_dialog is not None:
                    confirmation_mini_game_dialog.kill()
                    confirmation_mini_game_dialog = None
        else:
            # Создание сообщения для подтверждения входа в мини-игру
            create_confirmation_mini_game_dialog()


def create_confirmation_mini_game_dialog():

    """Создает диалог для подтверждения входа в мини-игру"""

    global confirmation_mini_game_dialog, player_stands_on_portal, current_game

    for i in portals:
        if pygame.sprite.collide_rect(player, i):
            current_game = i.game  # в current_game хранится название выбранной мини-игры

    if current_game != 'Выход':
        message = f'<font color="00FF00">Вы уверены, что хотите начать игру "{current_game}"?</font>'
    else:
        message = '<font color="00FF00">Вы уверены, что хотите покинуть лабиринт? Вернуться в него будет невозможно</font>'
    confirmation_mini_game_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((0, 0), (300, 200)),
        manager=manager,
        window_title='Подтверждение',
        action_long_desc=message,
        action_short_name='OK',
        blocking=True
    )
    confirmation_mini_game_dialog.confirm_button.colours[
        'normal_bg'] = pygame.Color((240, 240, 240, 255))
    confirmation_mini_game_dialog.confirm_button.colours[
        'hovered_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.confirm_button.colours[
        'active_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.confirm_button.colours[
        'normal_border'] = pygame.Color((255, 255, 255, 0))
    confirmation_mini_game_dialog.confirm_button.colours[
        'hovered_border'] = pygame.Color((0, 255, 0, 255))
    confirmation_mini_game_dialog.confirm_button.colours[
        'normal_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.confirm_button.colours[
        'hovered_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.confirm_button.rebuild()
    confirmation_mini_game_dialog.cancel_button.colours[
        'normal_bg'] = pygame.Color((240, 240, 240, 255))
    confirmation_mini_game_dialog.cancel_button.colours[
        'hovered_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.cancel_button.colours[
        'active_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.cancel_button.colours[
        'normal_border'] = pygame.Color((255, 255, 255, 0))
    confirmation_mini_game_dialog.cancel_button.colours[
        'hovered_border'] = pygame.Color((0, 255, 0, 255))
    confirmation_mini_game_dialog.cancel_button.colours[
        'normal_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.cancel_button.colours[
        'hovered_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.cancel_button.rebuild()
    confirmation_mini_game_dialog.title_bar.colours[
        'normal_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours[
        'hovered_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours[
        'active_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours[
        'normal_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.colours[
        'hovered_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.colours[
        'active_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.rebuild()
    confirmation_mini_game_dialog.background_colour = pygame.color.Color(
        (0, 200, 100))
    confirmation_mini_game_dialog.confirmation_text.background_colour = pygame.color.Color(
        (255, 255, 255))
    confirmation_mini_game_dialog.confirmation_text.rebuild()
    confirmation_mini_game_dialog.rebuild()
    player_stands_on_portal = True


def move(hero, movement):

    """Передвижение Деда Мороза"""

    x, y = hero.pos
    global level_x
    global level_y

    if movement == "up":
        hero.move((0, -0.05))
    elif movement == "down":
        hero.move((0, 0.05))
    elif movement == "left":
        hero.move((-0.05, 0))
    elif movement == "right":
        hero.move((0.05, 0))


def generate_level(level):

    """Обработка загруженного из файла уровня"""

    global MINI_GAMES

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
                AnimatedSprite('exit_portal', load_image("green_portal.png", -1), 4, 1,
                               x * tile_width, y * tile_height, 'Выход')
            elif level[y][x] == '*':
                Tile('empty', x, y)
                AnimatedSprite('portal', load_image("portal.png", -1), 4, 1,
                               x * tile_width, y * tile_height, MINI_GAMES[0])
                del MINI_GAMES[0]
            elif level[y][x] == '-':
                print('1')
                wall_group.add(Tile('empty', x, y))

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, level


class AnimatedSprite(pygame.sprite.Sprite):

    """Анимация порталов"""

    def __init__(self, type, sheet, columns, rows, x, y, game):

        super().__init__(all_sprites, portals)

        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.iter = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.game = game

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

    """Анимация Деда Мороза"""

    global animation_n, animation_i
    animation_n += 1
    if animation_n % 5 == 0:
        animation_i = (animation_i + 1) % 8
        player.change_picture(animation_i)


def draw_number_of_presents():

    """Выводит количество подарков в левом верхнем углу"""

    pygame.draw.rect(screen, 'white', (0, 0, 90, 45))
    pygame.draw.rect(screen, 'black', (0, 0, 90, 45), 2)

    font = pygame.font.Font(None, 50)
    string_rendered = font.render(str(number_of_presents), True,
                                  pygame.Color((0, 140, 0)))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = 12, 9
    screen.blit(string_rendered, intro_rect)


class Tile(pygame.sprite.Sprite):

    """Класс рисует клетку снега или камня"""

    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, wall_group)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):

    """Класс игрока"""

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos = [pos_x, pos_y]
        self.image = player_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 5, tile_height * pos_y + 5)

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

    """Обеспечивает передвижение камеры"""

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

    global user_name, user_time

    FPS = 60

    start_time = datetime.datetime.now()  # засекаем время начала для последующего отображения в правом верхнем углу \
    # и записи в бд
    font = pygame.font.SysFont('Consolas', 30)

    number_of_presents = 0  # количество собранных подарков

    MINI_GAMES = ['крестики-нолики',
                  'тетрис',
                  'змейка',
                  'сапёр',
                  '3 в ряд',
                  '2048',
                  'башня']  # список с названиями мини-игр
    shuffle(MINI_GAMES)
    current_game = None

    # Кадры для анимации Деда Мороза
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

    # Изображения для клеток и игрока
    tile_images = {
        'wall': load_image('walls.jpg'),
        'empty': load_image('floors.jpg')
    }
    player_image = animation_set[animation_i]

    # Изображение подарка (используется рядом с надписью с кол-вом подарком)
    present_image = pygame.sprite.Sprite()
    present_image_group = pygame.sprite.Group()
    present_image.image = load_image('present.jpg', -1)
    present_image.image = pygame.transform.scale(present_image.image, (40, 40))
    present_image.rect = present_image.image.get_rect()
    present_image.rect.x, present_image.rect.y = 40, 2
    present_image_group.add(present_image)

    # Размеры клетки
    tile_width = tile_height = 50

    # Инициализация экрана
    pygame.init()
    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('StolenPresents')

    # Запуск музыки
    pygame.mixer.music.load('data/Jingle Bells.mp3')
    pygame.mixer.music.play(loops=-1)

    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((width, height))

    # Запуск стартового экрана и слайд-шоу
    user_name = start_screen()
    show_history()

    # Загрузка уровня
    player, level_x, level_y, level_map = \
        generate_level(load_level('map2.txt'))

    size = width, height = 11 * tile_width, 11 * tile_height
    screen = pygame.display.set_mode(size)

    # Создание камеры
    camera = Camera()

    # Направления движения
    directions = {"right": False, "left": False, "up": False, "down": False}

    confirmation_mini_game_dialog = None

    player_stands_on_portal = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                add_to_database(user_name, number_of_presents, user_time)
                terminate()
            key = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_highscores()
                size = width, height = 550, 550
                screen = pygame.display.set_mode(size)
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                animation()
                # Движение игрока
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
            if event.type == pygame.USEREVENT:
                # обработка входа в мини-игры
                try:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        if current_game == 'крестики-нолики':
                            tic_tac_toe()
                            for i in portals:
                                if i.game == 'крестики-нолики':
                                    i.kill()
                        elif current_game == '3 в ряд':
                            game_three_in_row()
                            for i in portals:
                                if i.game == '3 в ряд':
                                    i.kill()
                        elif current_game == '2048':
                            game_2048()
                            for i in portals:
                                if i.game == '2048':
                                    i.kill()
                        elif current_game == 'сапёр':
                            saper()
                            for i in portals:
                                if i.game == 'сапёр':
                                    i.kill()
                        elif current_game == 'башня':
                            tower()
                            for i in portals:
                                if i.game == 'башня':
                                    i.kill()
                        elif current_game == 'змейка':
                            snake()
                            for i in portals:
                                if i.game == 'змейка':
                                    i.kill()
                            current_game = None
                        elif current_game == 'тетрис':
                            mini_game_tetris()
                            for i in portals:
                                if i.game == 'тетрис':
                                    i.kill()
                        elif current_game == 'Выход':
                            if number_of_presents == 7:
                                present_for_grinch()
                            presents_for_citizens()
                            show_highscores(True)
                except Exception as e:
                    print(e)

            manager.process_events(event)
        manager.update(60 / 1000)

        prepare_movement()

        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 0, 0))
        portals.update()

        all_sprites.draw(screen)
        portals.draw(screen)
        player_group.draw(screen)

        draw_number_of_presents()

        present_image_group.draw(screen)

        manager.draw_ui(screen)

        # Отображение времени, которое игрок находится в игре
        new_time = datetime.datetime.now()
        text = str(new_time - start_time)[:7]
        user_time = text
        screen.blit(font.render(text, True, (255, 0, 0)), (420, 10))

        pygame.display.flip()
        clock.tick(FPS)
