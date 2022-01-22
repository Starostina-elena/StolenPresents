import pygame
import sqlite3
import time
import os



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
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if transform:
        image = pygame.transform.scale(image, (40, 40))
    return image


def show_highscores():
    res = results()
    background_colour = (255,255,255)
    (width, height) = (550, 550)
    screen2 = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Результаты игры - топ 10')

    #fon = pygame.transform.scale(load_image('main_beginning_fon.jpg'), (800, 600))
    screen2.fill(pygame.Color('lightblue'))
    #screen2.blit(fon, (0, 0))

    font = pygame.font.Font(None, 28)
    start_y=100
    res.insert(0,['Игрок','Подарков','Время'])
    for i, line in enumerate(res[:10]):
        user = " ".join([str(a).strip().ljust(12, ' ') for a in line])
        print(user)
        string_rendered = font.render(user, 14, pygame.Color('white'))
        hs_rect=string_rendered.get_rect()
        hs_rect.y = i*30+start_y
        hs_rect.x = 50

        screen2.blit(string_rendered, hs_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                return
        pygame.display.flip()
        pygame.display.update()
    #time.sleep(10)

