import random

import pygame


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
            winner = 'Крестик'
        else:
            winner = 'Нолик'
        return winner
    else:
        is_not_winner = False
        for i in field:
            if i.count(0) != 0:
                is_not_winner = True
                break
        if not(is_not_winner):
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
        # self.click_count = 0
        self.game_status = True
        self.colors = [(0, 0, 0), (255, 0, 0), (0, 0, 255)]


    def text(self, message):
        intro_text = ''
        text_coord = 50
        print(message)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(message, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        print(text_coord)
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
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
            if not(check_field(self.board)):
                self.bot_turn()
            else:
                self.game_status = False
                print(check_field(self.board))
                self.text(check_field(self.board))


    def bot_turn(self):
        n = len(self.board)
        is_turn = False
        if not(is_turn):
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
        if not(is_turn):
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
        if not(is_turn):
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

size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.init()
board = Board(3, 3)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            try:
                board.get_click(event.pos)
            except Exception:
                pass
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
