import pygame
import pygame_gui

from random import randint


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[randint(0, 9) for j in range(width)] for i in range(height)]
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

        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

        self.player = 0

        self.chosen_cell = None

        self.blocked = False

        self.check_field_after_move()

        self.stones_left = 60
        
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
                if self.chosen_cell is not None and self.chosen_cell[0] == i and self.chosen_cell[1] == j:
                    color = 'white'
                else:
                    color = 'black'
                pygame.draw.rect(screen, color,
                                 (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                  self.cell_size - 2, self.cell_size - 2))
                if self.board[j][i] <= 9:
                    pygame.draw.ellipse(screen, self.colors[self.board[j][i]],
                                        (self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                                         self.cell_size - 2, self.cell_size - 2))

        if self.stones_left > 0:
            self.show_message(f'Камней разрушить осталось: {self.stones_left}', 40)
        else:
            self.show_message('Вы победили')
            if not self.win:
                show_rules('Благодаря вам Дед Мороз нашел 1 подарок!')
            self.win = True
            self.blocked = True

    def check_field_after_move(self):

        something_changed = False

        for _ in range(5):
            for i in range(self.width):
                for j in range(self.height):
                    try:
                        if self.board[j][i] == self.board[j][i + 1] == self.board[j][i + 2]:
                            something_changed = True
                            if i + 4 < self.width and self.board[j][i] == self.board[j][i + 1] == self.board[j][
                                i + 2] == \
                                    self.board[j][i + 3] == self.board[j][i + 4]:
                                for row in range(j, 0, -1):
                                    for column in range(i, i + 5):
                                        self.board[row][column] = self.board[row - 1][column]
                                for column in range(i, i + 5):
                                    self.board[0][column] = randint(0, 9)
                                self.stones_left -= 5
                            elif i + 3 < self.width and self.board[j][i] == self.board[j][i + 1] == self.board[j][
                                i + 2] == \
                                    self.board[j][i + 3]:
                                for row in range(j, 0, -1):
                                    for column in range(i, i + 4):
                                        self.board[row][column] = self.board[row - 1][column]
                                for column in range(i, i + 4):
                                    self.board[0][column] = randint(0, 9)
                                self.stones_left -= 4
                            else:
                                for row in range(j, 0, -1):
                                    for column in range(i, i + 3):
                                        self.board[row][column] = self.board[row - 1][column]
                                for column in range(i, i + 3):
                                    self.board[0][column] = randint(0, 9)
                                self.stones_left -= 3
                    except Exception:
                        pass
                    try:
                        if self.board[j][i] == self.board[j + 1][i] == self.board[j + 2][i]:
                            something_changed = True
                            if j + 4 < self.height and self.board[j][i] == self.board[j + 1][i] == self.board[j + 2][
                                i] == \
                                    self.board[j + 3][i] == self.board[j + 4][i]:
                                for row in range(j + 4, 4, -1):
                                    self.board[row][i] = self.board[row - 5][i]
                                for row in range(4, -1, -1):
                                    self.board[row][i] = randint(0, 9)
                                self.stones_left -= 5
                            elif j + 3 < self.height and self.board[j][i] == self.board[j + 1][i] == self.board[j + 2][
                                i] \
                                    == self.board[j + 3][i]:
                                for row in range(j + 3, 3, -1):
                                    self.board[row][i] = self.board[row - 4][i]
                                for row in range(3, -1, -1):
                                    self.board[row][i] = randint(0, 9)
                                self.stones_left -= 4
                            else:
                                for row in range(j + 2, 2, -1):
                                    self.board[row][i] = self.board[row - 3][i]
                                for row in range(2, -1, -1):
                                    self.board[row][i] = randint(0, 9)
                                self.stones_left -= 3
                    except Exception:
                        pass

        if not self.check_field_game_possible():
            self.show_message('Вы проиграли')
            self.blocked = True

        return something_changed

    def check_field_game_possible(self):

        for i in range(self.width):
            for j in range(self.height):
                try:
                    if self.board[j][i] == self.board[j + 1][i + 1] == self.board[j + 2][i]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j + 1][i + 1] == self.board[j][i + 2]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j - 1][i + 1] == self.board[j][i + 2]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j + 1][i - 1] == self.board[j + 2][i]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j][i + 1] == self.board[j][i + 3]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j][i + 2] == self.board[j][i + 3]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j + 1][i] == self.board[j + 3][i]:
                        return True
                except Exception:
                    pass
                try:
                    if self.board[j][i] == self.board[j + 2][i] == self.board[j + 3][i]:
                        return True
                except Exception:
                    pass
        return False

    def show_message(self, message, font_size=50):

        global width, screen

        font = pygame.font.Font(None, font_size)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
        screen.blit(string_rendered, intro_rect)

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and \
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height:
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        return None

    def on_click(self, cell_coords):
        if self.chosen_cell is not None:
            if cell_coords == self.chosen_cell:
                self.chosen_cell = None
            elif sorted([abs(cell_coords[0] - self.chosen_cell[0]), abs(cell_coords[1] - self.chosen_cell[1])]) == [0,
                                                                                                                    1]:
                self.board[self.chosen_cell[1]][self.chosen_cell[0]], self.board[cell_coords[1]][cell_coords[0]] = \
                    self.board[cell_coords[1]][cell_coords[0]], self.board[self.chosen_cell[1]][self.chosen_cell[0]]
                if not self.check_field_after_move():
                    self.board[self.chosen_cell[1]][self.chosen_cell[0]], self.board[cell_coords[1]][cell_coords[0]] = \
                        self.board[cell_coords[1]][cell_coords[0]], self.board[self.chosen_cell[1]][self.chosen_cell[0]]
                self.chosen_cell = None
            else:
                self.chosen_cell = cell_coords
        else:
            self.chosen_cell = cell_coords

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and not self.blocked:
            self.on_click(cell)


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
            rect=pygame.Rect((60, 60), (400, 350)),
            manager=manager,
            window_title='Правила',
            html_message='<font color="black">Перемещайте фигуры, чтобы создавать последовательности из одинаковых ' + \
                         'подряд идущих фигур длиной не менее 3. Перемещение фигур без успешного создания такой ' + \
                         'последовательности невозможно. Разбейте 60 фигур, чтобы победить! Создание на поле ' + \
                         'ситуации, когда перемещение невозможно, приведет к проигрышу</font>',
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

    board = Board(15, 15)
    board.set_view(35, 55, 32)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
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
