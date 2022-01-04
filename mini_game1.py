import random

import pygame
import pygame_gui


def check_field(field):
    n = len(field)
    is_winner = False
    for i in range(n):
        if not is_winner:
            if field[i][0] == field[i][1] == field[i][2] != 0:
                winner = field[i][0]
                is_winner = True
                break
            if field[0][i] == field[1][i] == field[2][i] != 0:
                winner = field[0][i]
                is_winner = True
                break
    if field[0][0] == field[1][1] == field[2][2] != 0:
        winner = field[0][0]
        is_winner = True
    if field[0][2] == field[1][1] == field[2][0] != 0:
        winner = field[0][2]
        is_winner = True
    if is_winner:
        if winner == 1:
            winner = 'Выиграл крестик'
        else:
            winner = 'Выиграл нолик'
        return winner
    else:
        is_not_winner = False
        for i in field:
            if i.count(0) != 0:
                is_not_winner = True
                break
        if not (is_not_winner):
            winner = 'Ничья'
            return winner


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 250
        self.top = 250
        self.cell_size = 80
        self.game_status = True
        self.colors = [(0, 0, 0), (255, 0, 0), (0, 0, 255)]

    def text(self, message):

        global width, screen

        font = pygame.font.Font(None, 80)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 100
        screen.blit(string_rendered, intro_rect)
        print('ok')

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 1:
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + x * self.cell_size + 2,
                                      self.top + y * self.cell_size + 2),
                                     (self.left + x * self.cell_size +
                                      self.cell_size - 2, self.top + y *
                                      self.cell_size + self.cell_size - 2),
                                     width=2)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + x * self.cell_size +
                                      self.cell_size - 2, self.top + y *
                                      self.cell_size + 2),
                                     (self.left + x * self.cell_size + 2,
                                      self.top + y * self.cell_size +
                                      self.cell_size - 2), width=2)
                elif self.board[y][x] == 2:
                    pygame.draw.circle(screen, (255, 0, 0),
                                       (self.left + x * self.cell_size +
                                        (self.cell_size / 2),
                                        self.top + y * self.cell_size +
                                        (self.cell_size / 2)),
                                       self.cell_size / 2 - 2, width=2)
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.left) // self.cell_size
        if cell_x not in range(0, 3) or cell_y not in range(0, 3):
            return None
        return (cell_y, cell_x)

    def on_click(self, cell_coords):
        if self.game_status:
            if self.board[cell_coords[0]][cell_coords[1]] == 0:
                self.board[cell_coords[0]][cell_coords[1]] = 1
            if not (check_field(self.board)):
                self.bot_turn()
            else:
                self.game_status = False
                print(check_field(self.board))
                self.text(check_field(self.board))

    def bot_turn(self):
        n = len(self.board)
        is_turn = False
        if not (is_turn):
            for i in range(n):
                if self.board[i].count(2) == 2 and not (is_turn):
                    for j in range(len(self.board[i])):
                        if self.board[i][j] != 2 and self.board[i][j] != 1:
                            self.board[i][j] = 2
                            is_turn = True
                            break
                if [self.board[0][i], self.board[1][i],
                    self.board[2][i]].count(2) == 2 and not (is_turn):
                    for j in range(len(self.board[i])):
                        if self.board[j][i] != 2 and self.board[j][i] != 1:
                            self.board[j][i] = 2
                            is_turn = True
                            break
            if [self.board[0][0], self.board[1][1],
                self.board[2][2]].count(2) == 2 and not (is_turn):
                for i in range(3):
                    if self.board[i][i] != 2 and self.board[i][i] != 1:
                        self.board[i][i] = 2
                        is_turn = True
                        break
            if [self.board[0][2], self.board[1][1],
                self.board[2][0]].count(2) == 2 and not (is_turn):
                for i in range(3):
                    if self.board[i][abs(i - 2)] != 2 and \
                            self.board[i][abs(i - 2)] != 1:
                        self.board[i][abs(i - 2)] = 2
                        is_turn = True
                        break
        for i in range(n):
            if self.board[i].count(1) == 2 and not (is_turn):
                for j in range(len(self.board[i])):
                    if self.board[i][j] != 2 and self.board[i][j] != 1:
                        self.board[i][j] = 2
                        is_turn = True
                        break
            if [self.board[0][i], self.board[1][i],
                self.board[2][i]].count(1) == 2 and not (is_turn):
                for j in range(len(self.board[i])):
                    if self.board[j][i] != 2 and self.board[j][i] != 1:
                        self.board[j][i] = 2
                        is_turn = True
                        break
        if [self.board[0][0], self.board[1][1],
            self.board[2][2]].count(1) == 2 and not (is_turn):
            for i in range(3):
                if self.board[i][i] != 2 and self.board[i][i] != 1:
                    self.board[i][i] = 2
                    is_turn = True
                    break
        if [self.board[0][2], self.board[1][1],
            self.board[2][0]].count(1) == 2 and not (is_turn):
            for i in range(3):
                if self.board[i][abs(i - 2)] != 2 and \
                        self.board[i][abs(i - 2)] != 1:
                    self.board[i][abs(i - 2)] = 2
                    is_turn = True
                    break
        if not (is_turn):
            for i in range(n):
                if self.board[i].count(2) > 0 and not (is_turn):
                    for j in range(len(self.board[i])):
                        if self.board[i][j] != 2 and self.board[i][j] != 1:
                            self.board[i][j] = 2
                            is_turn = True
                            break
                if [self.board[0][i], self.board[1][i],
                    self.board[2][i]].count(2) > 0 and not (is_turn):
                    for j in range(len(self.board[i])):
                        if self.board[j][i] != 2 and self.board[j][i] != 1:
                            self.board[j][i] = 2
                            is_turn = True
                            break
            if [self.board[0][0], self.board[1][1],
                self.board[2][2]].count(2) > 0 and not (is_turn):
                for i in range(3):
                    if self.board[i][i] != 2 and self.board[i][i] != 1:
                        self.board[i][i] = 2
                        is_turn = True
                        break
            if [self.board[0][2], self.board[1][1],
                self.board[2][0]].count(2) > 0 and not (is_turn):
                for i in range(3):
                    if self.board[i][abs(i - 2)] != 2 and \
                            self.board[i][abs(i - 2)] != 1:
                        self.board[i][abs(i - 2)] = 2
                        is_turn = True
                        break
        if not (is_turn):
            first_turn = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        first_turn.append([i, j])
            turn_coord = random.choice(first_turn)
            self.board[turn_coord[0]][turn_coord[1]] = 2
            is_turn = True
        if check_field(self.board):
            self.game_status = False
            print(check_field(self.board))
            self.text(check_field(self.board))


def start():

    global width, height, screen

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    board = Board(3, 3)
    running = True

    manager = pygame_gui.UIManager((width, height))

    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((750, 0), (50, 50)),
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    board.get_click(event.pos)
                except Exception:
                    pass
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == exit_button:
                        running = False
            manager.process_events(event)

        manager.update(60 / 1000)

        board.render(screen)

        manager.draw_ui(screen)

        pygame.display.flip()


# pygame.init()
# start()
