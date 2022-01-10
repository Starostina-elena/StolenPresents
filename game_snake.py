import pygame
import time
import random
import os
import sys

pygame.init()
clock = pygame.time.Clock()
width = 550
height = 550
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
snake_block = 10
snake_speed = 10
font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("arial", 35)
screen.fill('white')
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, 'pink')
    screen.blit(value, [180, 0])


def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, 'black', [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(messsage, [15, 15])

count = 0
game = True
x_snake = 225
y_snake = 225
x_food = random.randint(0, 500)
y_food = random.randint(50, 500)
x_plussnake = 1
y_plussnake = 1
snake_coords = []
play = 0
coords = [x_snake, y_snake]

def Game():
    global game, x_snake, y_snake, x_food, y_food, x_plussnake, y_plussnake, snake_coords, count
    if game == False:
        screen.fill('black')
        message("You Lost!", red)
        Your_score(count)
        pygame.display.update()
        time.sleep(3)
        exit()

def main():
    global game, x_snake, y_snake, x_food, y_food, x_plussnake, y_plussnake, snake_coords, count, coords
    if game:
        while game:
            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_plussnake = -snake_block
                        y_plussnake = 0
                    elif event.key == pygame.K_RIGHT:
                        x_plussnake = snake_block
                        y_plussnake = 0
                    elif event.key == pygame.K_UP:
                        y_plussnake = -snake_block
                        x_plussnake = 0
                    elif event.key == pygame.K_DOWN:
                        y_plussnake = snake_block
                        x_plussnake = 0
            if x_snake <= 0:
                x_snake = 550
            elif x_snake >= 550:
                x_snake = 0
            elif y_snake <= 0:
                y_snake = 550
            elif y_snake >= 550:
                y_snake = 0
            if (x_snake == x_food or x_snake == x_food - 1 or x_snake == x_food - 2 or x_snake == x_food - 3 or
                x_snake == x_food - 4 or x_snake == x_food - 5 or x_snake == x_food + 1 or x_snake == x_food + 2
            or x_snake == x_food + 3 or x_snake == x_food + 4 or x_snake == x_food + 5) and (y_snake == y_food or
            y_snake == y_food - 1 or y_snake == y_food - 2 or y_snake == y_food - 3 or y_snake == y_food - 4 or
            y_snake == y_food - 5 or y_snake == y_food + 1 or y_snake == y_food + 2 or y_snake == y_food + 3 or
            y_snake == y_food + 4 or y_snake == y_food + 5 or y_snake == y_food + 6 or y_snake == y_food + 7 or
            y_snake == y_food + 8 or y_snake == y_food + 9 or y_snake == y_food - 6 or y_snake == y_food - 7 or
            y_snake == y_food - 8 or y_snake == y_food - 9):
                x_food = random.randint(0, 500)
                y_food = random.randint(50, 500)
                screen.fill('white')
                pygame.draw.rect(screen, 'green', [x_food, y_food, 10, 10])
                count += 1
            clock.tick(snake_speed)
            x_snake += x_plussnake
            y_snake += y_plussnake
            screen.fill('white')
            pygame.draw.rect(screen, 'green', [x_food, y_food, 10, 10])
            snake_coords.append([x_snake, y_snake])
            if len(snake_coords) - 1:
                del snake_coords[0]
            our_snake(snake_block, snake_coords)
            Your_score(count)
            pygame.display.update()
    else:
        Game()

if __name__ == '__main__':
    pygame.init()
    main()
