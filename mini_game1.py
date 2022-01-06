import os
import random
import sys

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
                return ''
        if not (is_not_winner):
            winner = 'Ничья'
            return winner


def load_image(name, colorkey=-1, transform=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if transform:
        image = pygame.transform.scale(image, (70, 75))
    else:
        image = pygame.transform.scale(image, (245, 250))
    return image


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

        font = pygame.font.Font(None, 70)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
        screen.blit(string_rendered, intro_rect)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        all_sprites = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("поле.png", transform=False)
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = self.left - 5
        sprite.rect.y = self.top - 5
        all_sprites.draw(screen)
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 1:
                    all_sprites = pygame.sprite.Group()
                    sprite = pygame.sprite.Sprite()
                    sprite.image = load_image("крестик.png", transform=True)
                    sprite.rect = sprite.image.get_rect()
                    all_sprites.add(sprite)
                    sprite.rect.x = self.left + x * self.cell_size + 2
                    sprite.rect.y = self.top + y * self.cell_size + 2
                    all_sprites.draw(screen)
                elif self.board[y][x] == 2:
                    all_sprites = pygame.sprite.Group()
                    sprite = pygame.sprite.Sprite()
                    sprite.image = load_image("нолик.png", transform=True)
                    sprite.rect = sprite.image.get_rect()
                    all_sprites.add(sprite)
                    sprite.rect.x = self.left + x * self.cell_size + 2
                    sprite.rect.y = self.top + y * self.cell_size + 2
                    all_sprites.draw(screen)
        self.text(check_field(self.board))

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


def show_rules():

    global manager

    rules = pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((60, 0), (400, 175)),
        manager=manager,
        window_title='Правила',
        html_message='<font color="black">Играйте с компьютером: соберите ряд из трех крестиков, чтобы победить!'
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


def start():

    global width, height, screen, manager, confirmation_mini_game_dialog

    size = width, height = 550, 550
    screen = pygame.display.set_mode(size)
    board = Board(3, 3)
    board.set_view(155, 155, 80)
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
                        confirmation_exit_dialog()
                    elif event.ui_element == help_button:
                        show_rules()
                elif event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    if event.ui_element == confirmation_mini_game_dialog:
                        running = False
            manager.process_events(event)

        screen.fill((0, 0, 0))

        manager.update(60 / 1000)

        board.render(screen)

        manager.draw_ui(screen)

        pygame.display.flip()


if __name__ == '__main__':

    pygame.init()
    start()