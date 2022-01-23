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


def show_highscores():
    # вывод результатов игры
    res = results()
    background_colour = (255, 255, 255)
    (width, height) = (550, 550)
    screen2 = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Результаты игры - топ 10')

    screen2.fill(pygame.Color('lightblue'))

    font = pygame.font.Font(None, 28)
    start_y = 100
    res.insert(0, ['Игрок', 'Подарков', 'Время'])
    for i, line in enumerate(res[:10]):
        user = " ".join([str(a).strip().ljust(18, ' ') for a in line])
        print(user)
        string_rendered = font.render(user, 14, pygame.Color('white'))
        hs_rect = string_rendered.get_rect()
        hs_rect.y = i * 30 + start_y
        hs_rect.x = 50

        screen2.blit(string_rendered, hs_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.display.update()
