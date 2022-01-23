import pygame
import sqlite3
import time
import os
import sys


def open_database():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    return con, cur


def add_to_database(name, score, time):
    con, cur = open_database()
    result = cur.execute("""INSERT INTO information(name, score, time) VALUES(?, ?, ?)""",
                         (name, score, time))
    result.fetchall()
    con.commit()


def results():
    con, cur = open_database()
    result = cur.execute("""SELECT name, score, time FROM information ORDER BY score DESC, time ASC""")
    return result.fetchall()


def load_image(name, colorkey=0, transform=None):
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


def show_highscores(mode=False):
    # вывод результатов
    res = results()
    background_colour = (255, 255, 255)
    (width, height) = (550, 550)
    screen2 = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Результаты игры - топ 10')

    screen2.fill(pygame.Color('lightblue'))

    font = pygame.font.Font(None, 28)
    start_y = 100
    res.insert(0, ['Игрок', 'Подарков', 'Время'])
    for i, line in enumerate(res[:11]):
        user = line[0]
        gifts = line[1]
        time = line[2]
        print(user, gifts, time)

        user_rendered = font.render(user, 14, pygame.Color('white'))
        user_rect = user_rendered.get_rect()
        user_rect.y = i * 30 + start_y
        user_rect.x = 20

        gifts_rendered = font.render(str(gifts), 14, pygame.Color('white'))
        gifts_rect = gifts_rendered.get_rect()
        gifts_rect.y = i * 30 + start_y
        gifts_rect.x = 270

        time_rendered = font.render(str(time), 14, pygame.Color('white'))
        time_rect = time_rendered.get_rect()
        time_rect.y = i * 30 + start_y
        time_rect.x = 400

        screen2.blit(user_rendered, user_rect)
        screen2.blit(gifts_rendered, gifts_rect)
        screen2.blit(time_rendered, time_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Если mode=True, окно нельзя закрыть пробелом
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not mode:
                return
        pygame.display.flip()
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    show_highscores()
