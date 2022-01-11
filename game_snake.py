import pygame
import time
import random
import os
import sys
import pygame_gui

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
    mess = font_style.render(msg, True, color)
    screen.blit(mess, [200, 225])

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
        if count >= 7:
            screen.fill('white')
            message("You Win!", "red")
            Your_score(count)
            pygame.display.update()
            time.sleep(3)
            exit()
        else:
            screen.fill('white')
            message("You Lost!", "red")
            Your_score(count)
            pygame.display.update()
            time.sleep(3)
            exit()

def show_rules(message=None):
    global manager

    if message:
        rules = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((60, 60), (300, 175)),
            manager=manager,
            window_title='',
            html_message=f'<font color="black">{message}</font>',
        )
    else:
        rules = pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect((60, 60), (400, 400)),
            manager=manager,
            window_title='Правила',
            html_message='<font color="black">Ваша задача: собирать еду для вашей змейки ' + \
                         '(маленькие квадратики). У вас есть минута, чтобы собрать 7 квадратиков ' + \
                         'Если вы собираете меньше - проигрыш ' + \
                         'Удачной игры!</font>',
        )
    rules.dismiss_button.text = 'Закрыть'
    rules.dismiss_button.colours['normal_bg'] = pygame.Color((240, 240, 240, 255))
    rules.dismiss_button.colours['hovered_bg'] = pygame.Color((255, 255, 255, 255))
    rules.dismiss_button.colours['active_bg'] = pygame.Color((255, 255, 255, 255))
    rules.dismiss_button.colours['normal_border'] = pygame.Color((255, 255, 255, 0))
    rules.dismiss_button.colours['hovered_border'] = pygame.Color((0, 255, 0, 255))
    rules.dismiss_button.colours['normal_text'] = pygame.Color((255, 40, 40, 255))
    rules.dismiss_button.colours['hovered_text'] = pygame.Color((255, 40, 40, 255))
    rules.dismiss_button.rebuild()
    rules.title_bar.colours['normal_bg'] = pygame.Color((0, 200, 100))
    rules.title_bar.colours['hovered_bg'] = pygame.Color((0, 200, 100))
    rules.title_bar.colours['active_bg'] = pygame.Color((0, 200, 100))
    rules.title_bar.colours['normal_text'] = pygame.Color((0, 0, 0))
    rules.title_bar.colours['hovered_text'] = pygame.Color((0, 0, 0))
    rules.title_bar.colours['active_text'] = pygame.Color((0, 0, 0))
    rules.title_bar.rebuild()
    rules.background_colour = pygame.color.Color((0, 200, 100))
    rules.text_block.background_colour = pygame.color.Color((255, 255, 255))
    rules.text_block.rebuild()
    rules.rebuild()


def confirmation_exit_dialog():
    global manager, confirmation_mini_game_dialog

    confirmation_mini_game_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((200, 70), (300, 200)),
        manager=manager,
        window_title='Подтверждение',
        action_long_desc=f'<font color="00FF00">Вы уверены, что хотите выйти? Вернуться в мини-игру будет невозможно</font>',
        action_short_name='OK',
        blocking=True
    )
    confirmation_mini_game_dialog.confirm_button.colours['normal_bg'] = pygame.Color((240, 240, 240, 255))
    confirmation_mini_game_dialog.confirm_button.colours['hovered_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.confirm_button.colours['active_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.confirm_button.colours['normal_border'] = pygame.Color((255, 255, 255, 0))
    confirmation_mini_game_dialog.confirm_button.colours['hovered_border'] = pygame.Color((0, 255, 0, 255))
    confirmation_mini_game_dialog.confirm_button.colours['normal_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.confirm_button.colours['hovered_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.confirm_button.rebuild()
    confirmation_mini_game_dialog.cancel_button.colours['normal_bg'] = pygame.Color((240, 240, 240, 255))
    confirmation_mini_game_dialog.cancel_button.colours['hovered_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.cancel_button.colours['active_bg'] = pygame.Color((255, 255, 255, 255))
    confirmation_mini_game_dialog.cancel_button.colours['normal_border'] = pygame.Color((255, 255, 255, 0))
    confirmation_mini_game_dialog.cancel_button.colours['hovered_border'] = pygame.Color((0, 255, 0, 255))
    confirmation_mini_game_dialog.cancel_button.colours['normal_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.cancel_button.colours['hovered_text'] = pygame.Color((255, 40, 40, 255))
    confirmation_mini_game_dialog.cancel_button.rebuild()
    confirmation_mini_game_dialog.title_bar.colours['normal_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours['hovered_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours['active_bg'] = pygame.Color((0, 200, 100))
    confirmation_mini_game_dialog.title_bar.colours['normal_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.colours['hovered_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.colours['active_text'] = pygame.Color((0, 0, 0))
    confirmation_mini_game_dialog.title_bar.rebuild()
    confirmation_mini_game_dialog.background_colour = pygame.color.Color((0, 200, 100))
    confirmation_mini_game_dialog.confirmation_text.background_colour = pygame.color.Color((255, 255, 255))
    confirmation_mini_game_dialog.confirmation_text.rebuild()
    confirmation_mini_game_dialog.rebuild()


def main():
    global game, x_snake, y_snake, x_food, y_food, x_plussnake, y_plussnake, snake_coords, count, coords, \
        width, height, screen, manager, confirmation_mini_game_dialog
    manager = pygame_gui.UIManager((width, height))

    current_block_id = None
    time = True

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((500, 0), (50, 50)),
        text='X',
        manager=manager
    )
    exit_button.colours['normal_bg'] = pygame.Color((240, 240, 240, 255))
    exit_button.colours['hovered_bg'] = pygame.Color((255, 255, 255, 255))
    exit_button.colours['active_bg'] = pygame.Color((255, 255, 255, 255))
    exit_button.colours['normal_border'] = pygame.Color((255, 255, 255, 0))
    exit_button.colours['hovered_border'] = pygame.Color((0, 255, 0, 255))
    exit_button.colours['normal_text'] = pygame.Color((255, 0, 0, 255))
    exit_button.colours['hovered_text'] = pygame.Color((255, 0, 0, 255))
    exit_button.rebuild()

    help_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 0), (50, 50)),
        text='?',
        manager=manager
    )
    help_button.colours['normal_bg'] = pygame.Color((240, 240, 240, 255))
    help_button.colours['hovered_bg'] = pygame.Color((255, 255, 255, 255))
    help_button.colours['active_bg'] = pygame.Color((255, 255, 255, 255))
    help_button.colours['normal_border'] = pygame.Color((255, 255, 255, 0))
    help_button.colours['hovered_border'] = pygame.Color((0, 255, 0, 255))
    help_button.colours['normal_text'] = pygame.Color((255, 0, 0, 255))
    help_button.colours['hovered_text'] = pygame.Color((255, 0, 0, 255))
    help_button.rebuild()
    clock = pygame.time.Clock()
    running = True
    status_game_blocked = False
    while running:
        screen.fill('white')
        pygame.draw.rect(screen, 'green', [x_food, y_food, 10, 10])
        our_snake(snake_block, snake_coords)
        Your_score(count)
        t = clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        confirmation_exit_dialog()
                        status_game_blocked = True
                    elif event.ui_element == help_button:
                        show_rules()
                        status_game_blocked = True
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_mini_game_dialog:
                        running = False
                elif event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                    status_game_blocked = False
            manager.process_events(event)
        counter, text = 60, '10'.rjust(3)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        font = pygame.font.SysFont('Consolas', 30)

        if game:
            while game:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT:
                        counter -= 1
                        if counter > 0:
                            text = str(counter).rjust(3)
                        else:
                            'boom!'
                            game = False
                    if event.type == pygame.QUIT:
                        break
                else:
                    screen.blit(font.render(text, True, (0, 0, 0)), (80, 0))
                    pygame.display.flip()
                    clock.tick(60)
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
                    or x_snake == x_food + 3 or x_snake == x_food + 4 or x_snake == x_food + 5) and (
                        y_snake == y_food or
                        y_snake == y_food - 1 or y_snake == y_food - 2 or y_snake == y_food - 3 or y_snake == y_food - 4 or
                        y_snake == y_food - 5 or y_snake == y_food + 1 or y_snake == y_food + 2 or y_snake == y_food + 3 or
                        y_snake == y_food + 4 or y_snake == y_food + 5 or y_snake == y_food + 6 or y_snake == y_food + 7 or
                        y_snake == y_food + 8 or y_snake == y_food + 9 or y_snake == y_food - 6 or y_snake == y_food - 7 or
                        y_snake == y_food - 8 or y_snake == y_food - 9):
                    x_food = random.randint(0, 500)
                    y_food = random.randint(50, 500)
                    count += 1
                clock.tick(snake_speed)
                x_snake += x_plussnake
                y_snake += y_plussnake
                screen.fill('white')
                pygame.draw.rect(screen, 'green', [x_food, y_food, 10, 10])
                snake_coords.append([x_snake, y_snake])
                if len(snake_coords) - 1 > count:
                    del snake_coords[0]
                our_snake(snake_block, snake_coords)
                Your_score(count)
                pygame.display.update()
        else:
            Game()
        manager.update(60 / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
