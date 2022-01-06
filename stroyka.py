import pygame
import sys
import os

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Mountain(pygame.sprite.Sprite):


    image = load_image("moun.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = height

mountain = Mountain()
y_pos = 213
my = []
count = 0

class Landing(pygame.sprite.Sprite):
    image = load_image("kvaddd.png")
    def __init__(self, pos):
        global my, y_pos, count
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        res = 0
        my += [self.rect.x, self.rect.y]
        print(my)
        count += 1
        if count != 1:
            y_pos -= 25

    def update(self):
        global y_pos, count, res
        if not pygame.sprite.collide_mask(self, mountain) and self.rect.y < y_pos:
            self.rect = self.rect.move(0, 1)
        if count != 1:
            if abs(int(my[-2]) - int(my[0])) > 12:
                print("Game over")
                exit()



clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))
    t = clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            Landing(event.pos)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
