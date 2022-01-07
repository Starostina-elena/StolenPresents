import pygame
import pygame_gui

from random import randint, choice


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[None for j in range(width)] for i in range(height)]

        x1, y1, x2, y2 = randint(0, 3), randint(0, 3), randint(0, 3), randint(0, 3)
        while x1 == x2 and y1 == y2:
            x2, y2 = randint(0, 3), randint(0, 3)
        self.board[x1][y1] = choice([2, 4])
        self.board[x2][y2] = choice([2, 4])

        self.colors = {
            2: '#FFD773',
            4: '#FFC840',
            8: '#FFB600',
            16: '#FF9500',
            32: '#FF7C00',
            64: '#FF5900',
            128: '#FF3900',
            256: '#FB000D',
        }

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        self.blocked = False

        self.win = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):

        pygame.draw.rect(screen, 'white', ((self.left, self.top),
                                           (self.width * self.cell_size, self.height * self.cell_size)))

        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i]:
                    pygame.draw.rect(screen, self.colors[self.board[j][i]],
                                     (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                      self.cell_size - 2, self.cell_size - 2))
                    if len(str(self.board[j][i])) == 1:
                        font = pygame.font.Font(None, 140)
                        string_rendered = font.render(str(self.board[j][i]), True, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x, intro_rect.y = i * self.cell_size + 30 + self.left, j * self.cell_size + 15 + self.top
                        screen.blit(string_rendered, intro_rect)
                    elif len(str(self.board[j][i])) == 2:
                        font = pygame.font.Font(None, 120)
                        string_rendered = font.render(str(self.board[j][i]), True, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x, intro_rect.y = i * self.cell_size + 15 + self.left, j * self.cell_size + 20 + self.top
                        screen.blit(string_rendered, intro_rect)
                    else:
                        font = pygame.font.Font(None, 100)
                        string_rendered = font.render(str(self.board[j][i]), True, pygame.Color('white'))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.x, intro_rect.y = i * self.cell_size + 1 + self.left, j * self.cell_size + 20 + self.top
                        screen.blit(string_rendered, intro_rect)
                else:
                    pygame.draw.rect(screen, 'black',
                                     (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                      self.cell_size - 2, self.cell_size - 2))

                if self.board[j][i] == 256:
                    pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
                    self.show_message('Вы победили')
                    if not self.win:
                        show_rules('Благодаря вам Дед Мороз нашел 1 подарок!')
                    self.win = True
                    self.blocked = True
                elif not self.blocked:
                    self.show_message('Цель: 256')

    def check_field_game_possible(self):

        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] is None:
                    return True
                if j + 1 < self.height and self.board[j][i] == self.board[j + 1][i] or \
                        j - 1 >= 0 and self.board[j][i] == self.board[j - 1][i] or \
                        i + 1 < self.width and self.board[j][i] == self.board[j][i + 1] or \
                        i - 1 >= 0 and self.board[j][i] == self.board[j][i - 1]:
                    return True

        return False

    def show_message(self, message, font_size=50):

        global width, screen

        font = pygame.font.Font(None, font_size)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
        screen.blit(string_rendered, intro_rect)

    def move(self, coords):

        if self.blocked:
            return

        if coords == (0, 1):
            for _ in range(4):
                for i in range(self.width):
                    for j in range(self.height - 1, 0, -1):
                        if self.board[j][i] is not None and self.board[j][i] == self.board[j - 1][i]:
                            self.board[j][i] = self.board[j][i] * 2
                            self.board[j - 1][i] = None
                        if self.board[j][i] is None:
                            self.board[j][i] = self.board[j - 1][i]
                            self.board[j - 1][i] = None
        elif coords == (0, -1):
            for _ in range(4):
                for i in range(self.width):
                    for j in range(self.height - 1):
                        if self.board[j][i] is not None and self.board[j][i] == self.board[j + 1][i]:
                            self.board[j][i] = self.board[j][i] * 2
                            self.board[j + 1][i] = None
                        if self.board[j][i] is None:
                            self.board[j][i] = self.board[j + 1][i]
                            self.board[j + 1][i] = None
        elif coords == (1, 0):
            for _ in range(4):
                for i in range(self.width - 1, 0, -1):
                    for j in range(self.height):
                        if self.board[j][i] is not None and self.board[j][i] == self.board[j][i - 1]:
                            self.board[j][i] = self.board[j][i] * 2
                            self.board[j][i - 1] = None
                        if self.board[j][i] is None:
                            self.board[j][i] = self.board[j][i - 1]
                            self.board[j][i - 1] = None
        else:
            for _ in range(4):
                for i in range(self.width - 1):
                    for j in range(self.height):
                        if self.board[j][i] is not None and self.board[j][i] == self.board[j][i + 1]:
                            self.board[j][i] = self.board[j][i] * 2
                            self.board[j][i + 1] = None
                        if self.board[j][i] is None:
                            self.board[j][i] = self.board[j][i + 1]
                            self.board[j][i + 1] = None

        empty_cells_coords = []

        for i in range(self.width):
            for j in range(self.height):
                if self.board[j][i] is None:
                    empty_cells_coords.append((j, i))

        if empty_cells_coords:
            y, x = choice(empty_cells_coords)
            self.board[y][x] = choice([2, 4])

        if not self.check_field_game_possible():
            pygame.draw.rect(screen, 'black', (60, 0, 400, 50))
            self.show_message('Вы проиграли')
            self.blocked = True


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
            html_message='<font color="black">Перемещайте фигуры с помощью стрелок на клавиатуре. ' + \
                         'Когда вы нажимаете на кнопку, все числа на поле сдвигаются в указанном направлении. ' + \
                         'Когда одинаковые числа наезжают друг на друга, они "собираются" в одно удвоенное. ' + \
                         'Каждый ход на поле в случайном месте появляется новое число. ' + \
                         'Соберите число 256, чтобы победить! Создание на поле ситуации, когда движение невозможно, ' + \
                         'приведет к проигрышу.</font>',
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

    global width, height, screen, manager, confirmation_mini_game_dialog

    width, height = 550, 550
    screen = pygame.display.set_mode((width, height))

    board = Board(4, 4)
    board.set_view(35, 60, 120)
    running = True

    manager = pygame_gui.UIManager((width, height))

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

    fps = 20
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.key.key_code('left'):
                    board.move((-1, 0))
                if event.key == pygame.key.key_code('right'):
                    board.move((1, 0))
                if event.key == pygame.key.key_code('up'):
                    board.move((0, -1))
                if event.key == pygame.key.key_code('down'):
                    board.move((0, 1))
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        confirmation_exit_dialog()
                    elif event.ui_element == help_button:
                        show_rules()
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_mini_game_dialog:
                        running = False
            manager.process_events(event)

        if not board.blocked:
            screen.fill((0, 0, 0))

        manager.update(60 / 1000)

        board.render(screen)

        manager.draw_ui(screen)

        clock.tick(fps)
        pygame.display.flip()

    return board.win


if __name__ == '__main__':
    pygame.init()
    main()
