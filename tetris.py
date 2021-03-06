import pygame
import pygame_gui

from random import randint, choice
from copy import deepcopy

import sys


class Board:

    """Реализует доску, на которой расположены все фигуры"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # изначально доска пуста
        self.board = [[None for j in range(width)] for i in range(height)]

        # цвета, используемые для окраски фигур
        self.colors = [(0, 255, 200),
                       (255, 255, 0),
                       (150, 200, 0),
                       (230, 0, 230),
                       (0, 150, 0),
                       (230, 0, 0),
                       (0, 0, 200),
                       (0, 100, 100),
                       (100, 255, 70),
                       (70, 100, 255)]

        # возможные конфигурации фигур
        self.figures = [
            ((1, 0, 0), (1, 1, 1)),
            ((1, 1, 1, 1),),
            ((1, 1), (1, 1)),
            ((0, 0, 1), (1, 1, 1)),
            ((1, 1, 0), (0, 1, 1)),
            ((0, 1, 0), (1, 1, 1)),
            ((0, 1, 1), (1, 1, 0))
        ]

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        # блокирует игру до начала и после завершения
        self.blocked = True
        self.after_start = True

        self.show_message('Нажмите пробел, чтобы начать', 40)

        # для победы нужно собрать 5 строк
        self.rows_left = 5

        self.win = False

        # в этом списке хранятся кортежи с координатами элементов текущего (падающего) блока
        self.current_block = []

    def set_view(self, left, top, cell_size):

        """Задает координаты левого верхнего угла доски и размер клетки"""

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):

        """Отрисовка доски"""

        pygame.draw.rect(screen, 'white', ((self.left, self.top),
                                           (self.width * self.cell_size, self.height * self.cell_size)))

        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, 'black',
                                 (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                  self.cell_size - 2, self.cell_size - 2))
                if self.board[j][i] is not None and self.board[j][i] <= 9:
                    pygame.draw.rect(screen, self.colors[self.board[j][i]],
                                     (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                      self.cell_size - 2, self.cell_size - 2))

        pygame.draw.line(screen, 'red', (self.left, self.top + self.cell_size * 2),
                         (self.left + self.cell_size * self.width, self.top + self.cell_size * 2), 3)

        if self.rows_left > 0:
            if not self.blocked:
                self.show_message(f'Строк разрушить осталось: {self.rows_left}', 40)
        else:
            self.show_message('Вы победили')
            # эта проверка нужна, чтобы сообщение о победе показывалось только 1 раз
            if not self.win:
                show_rules('Благодаря вам Дед Мороз нашел 1 подарок!')
            self.win = True
            self.blocked = True

    def update(self):

        """Если блок может целиком сдвинуться на 1 клетку вниз, сдвигает его"""

        moved = True

        for i in sorted(self.current_block, key=lambda el: -el[0]):
            try:
                if self.board[i[0] + 1][i[1]] is not None and (i[0] + 1, i[1]) not in self.current_block:
                    moved = False
            except Exception:
                moved = False

        if moved:
            for i in self.current_block:
                block_color = self.board[i[0]][i[1]]
                self.board[i[0]][i[1]] = None
            for i in range(len(self.current_block)):
                self.current_block[i] = (self.current_block[i][0] + 1, self.current_block[i][1])
            for i in self.current_block:
                self.board[i[0]][i[1]] = block_color
        else:
            self.new_block()

        self.check_field_after_move()
    
    def move(self, direction):

        """Перемещение текущего блока вправо/влево"""

        moved = True

        for i in sorted(self.current_block, key=lambda el: -el[0]):
            try:
                if self.board[i[0] + direction[0]][i[1] + direction[1]] is not None and \
                        (i[0] + direction[0], i[1] + direction[1]) not in self.current_block or \
                        i[0] + direction[0] < 0 or i[0] + direction[0] >= self.height or \
                        i[1] + direction[1] < 0 or i[1] + direction[1] >= self.height:
                    moved = False
            except Exception:
                moved = False

        if moved:
            for i in self.current_block:
                block_color = self.board[i[0]][i[1]]
                self.board[i[0]][i[1]] = None
            for i in range(len(self.current_block)):
                self.current_block[i] = (self.current_block[i][0] + direction[0], self.current_block[i][1] + direction[1])
            for i in self.current_block:
                self.board[i[0]][i[1]] = block_color

        self.check_field_after_move()
    
    def spin(self):

        """Вращение блока"""

        x, y = min(self.current_block, key=lambda el: el[1])[1], min(self.current_block, key=lambda el: el[0])[0]
        block_coords = [(i[0] - y, i[1] - x) for i in self.current_block]
        block_width, block_height = max(block_coords, key=lambda el: el[1])[1] + 1, max(block_coords, key=lambda el: el[0])[0] + 1
        block = [[1 if (j, i) in block_coords else 0 for i in range(block_width)] for j in range(block_height)]

        new_block = []
        for i in range(len(block[0])):
            line = []
            for j in range(len(block)):
                line.append(block[j][i])
            new_block.append(line)

        board_copy = deepcopy(self.board)

        for i in self.current_block:
            board_copy[i[0]][i[1]] = None

        can_place = True
        for i in range(len(new_block)):
            for j in range(len(new_block[0])):
                try:
                    if board_copy[i + y][j + x] is not None and new_block[i][j]:
                        can_place = False
                except Exception:
                    can_place = False

        if can_place:
            for i in self.current_block:
                block_color = self.board[i[0]][i[1]]
                self.board[i[0]][i[1]] = None
            self.current_block = []
            for i in range(len(new_block)):
                for j in range(len(new_block[0])):
                    if new_block[i][j]:
                        self.board[i + y][j + x] = block_color
                        self.current_block.append((i + y, j + x))

    def check_field_after_move(self):

        """Уничтожает собранные строки"""

        for i in range(len(self.board)):
            if self.board[i].count(None) == 0:
                self.board[i] = [None for _ in range(self.width)]
                self.rows_left -= 1
                for move_i in range(i, 0, -1):
                    for j in range(self.width):
                        self.board[move_i][j], self.board[move_i - 1][j] = self.board[move_i - 1][j], None

        if not self.check_field_game_possible():
            screen.fill((0, 0, 0))
            self.show_message('Вы проиграли')
            self.blocked = True

    def check_field_game_possible(self):

        """Проверяет, что блоки не заходят за красную линию"""

        for row in range(self.height):
            for column in range(self.width):
                if row <= 1 and self.board[row][column] is not None and (row, column) not in self.current_block:
                    return False
                if row > 1 and self.board[row][column] is None:
                    return True
        return False
    
    def new_block(self):

        """Создание нового блока"""

        block = choice(self.figures)
        block_color = randint(0, 9)

        self.current_block = []

        x_pos = (self.width - len(block[0])) // 2
        for i in range(len(block)):
            for j in range(len(block[i])):
                if block[i][j]:
                    self.board[i][j + x_pos] = block_color
                    self.current_block.append((i, j + x_pos))

    def show_message(self, message, font_size=50):

        """Вывод надписи над доской"""

        global width, screen

        font = pygame.font.Font(None, font_size)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
        screen.blit(string_rendered, intro_rect)


def show_rules(message=None):

    """Создает окно с помощью pygame_gui и выводит в него либо правила,
    либо сообщение о начислении подарка за победу"""

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
            rect=pygame.Rect((60, 60), (400, 350)),
            manager=manager,
            window_title='Правила',
            html_message='<font color="black">Используйте стрелки "влево" и "вправо" на клавиатуре, ' + \
                         'чтобы сдвинуть блок в сторону и пробел, чтобы повернуть его. Когда вы полностью ' + \
                         'заполните строку, эта строка исчезнет. Разбейте 15 строк, чтобы победить! ' + \
                         'Если в какой-то момент один из блоков окажется над чертой, вы проиграете.</font>',
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

    """Создание окна для подтверждения выхода из игры"""

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

    """Основная функция, которая вызывается в main.py"""

    global width, height, screen, manager, confirmation_mini_game_dialog

    width, height = 550, 550
    screen = pygame.display.set_mode((width, height))

    board = Board(15, 15)
    board.set_view(35, 55, 32)
    running = True

    manager = pygame_gui.UIManager((width, height))

    # Создание кнопки для возврата в лабиринт
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

    # Создание кнопки помощи
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

    fps = 4
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        confirmation_exit_dialog()
                    elif event.ui_element == help_button:
                        show_rules()
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_mini_game_dialog:
                        running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 32:  # 32 - код пробела
                    if board.after_start:
                        board.after_start = False
                        board.blocked = False
                        board.new_block()
                    else:
                        board.spin()
                elif event.key == pygame.key.key_code('right'):
                    board.move((0, 1))
                elif event.key == pygame.key.key_code('left'):
                    board.move((0, -1))
            manager.process_events(event)

        if not board.blocked:
            screen.fill((0, 0, 0))
            board.update()

        manager.update(60 / 1000)

        board.render(screen)

        manager.draw_ui(screen)

        clock.tick(fps)
        pygame.display.flip()

    return board.win


if __name__ == '__main__':
    pygame.init()
    main()
