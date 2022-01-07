import pygame
import sys
import os
import pygame_gui

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
result = 0



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
        global my, y_pos, count, result
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        print(count, result, my, 1)

    def update(self):
        try:
            global y_pos, count, result, my
            if event.type == pygame.MOUSEBUTTONDOWN and count != 1:
                my += [self.rect.x, self.rect.y]
                count += 1
                if count != 1:
                    y_pos -= 25
            print(count, result, my, 2)
            if result % 2 != 0:
                self.rect.x += 5
                if self.rect.left > width:
                    self.rect.right = 0
            else:
                if not pygame.sprite.collide_mask(self, mountain) and self.rect.y < y_pos:
                    self.rect = self.rect.move(0, 1)
                else:
                    Landing([122, 20])
                if count != 0:
                    if abs(int(my[-2]) - int(my[0])) > 12:
                        print("Game over")
                        exit()
        except Exception as a:
            print(a)


clock = pygame.time.Clock()
running = True
while running:
    screen.fill((255, 255, 255))
    t = clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            result += 1
            if result == 1:
                Landing(event.pos)
            else:
                all_sprites.update()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
