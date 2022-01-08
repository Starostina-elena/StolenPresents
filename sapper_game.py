import os
import random
import sys
from copy import deepcopy

import pygame
import pygame_gui


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
        image = pygame.transform.scale(image, (30, 30))
    else:
        image = pygame.transform.scale(image, (144, 144))
    return image

def check_win(board):
    is_win = 'OK'
    for i in board:
        if i.count('') > 0:
            is_win = False
        if 'boom' in i:
            is_win = 'Finish'
            break
    if is_win == 'OK':
        return 'Вы победили'
    elif is_win == 'Finish':
        return 'Вы проиграли'

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[''] * width for _ in range(height)]
        self.show_board = deepcopy(self.board)

        # значения по умолчанию
        self.left = 150
        self.top = 50
        self.cell_size = 45
        self.game_status = True
        self.colors = [(0, 0, 0), (255, 0, 0), (0, 0, 255)]
        self.n_bomb = 5
        self.generation_bomb()
        self.place_number()

    def text_number(self, message, x, y):

        global width, screen

        font = pygame.font.Font(None, 40)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = x, y
        screen.blit(string_rendered, intro_rect)

    def text(self, message):
        global width, screen
        font = pygame.font.Font(None, 40)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = 200, 350
        screen.blit(string_rendered, intro_rect)

    def generation_bomb(self):
        for i in range(self.n_bomb):
            self.board[random.randint(0, 6 - 1)][random.randint(0, 6 - 1)] = 'b'
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
        sprite.rect.x = self.left + 130
        sprite.rect.y = self.top - 5
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("поле.png", transform=False)
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = self.left - 5
        sprite.rect.y = self.top - 5
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("поле.png", transform=False)
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = self.left - 5
        sprite.rect.y = self.top + 130
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image("поле.png", transform=False)
        sprite.rect = sprite.image.get_rect()
        all_sprites.add(sprite)
        sprite.rect.x = self.left + 130
        sprite.rect.y = self.top + 130
        all_sprites.draw(screen)
        for x in range(self.width):
            for y in range(self.height):
                pass
                if self.show_board[y][x] == '':
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + x * self.cell_size + 2,
                                      self.top + y * self.cell_size + 2,
                                      self.cell_size - 2, self.cell_size - 2), 0)
                if self.show_board[y][x] == 'boom':
                    all_sprites = pygame.sprite.Group()
                    sprite = pygame.sprite.Sprite()
                    sprite.image = load_image("boom.png", transform=True)
                    sprite.rect = sprite.image.get_rect()
                    all_sprites.add(sprite)
                    sprite.rect.x = self.left + x * self.cell_size + 9
                    sprite.rect.y = self.top + y * self.cell_size + 9
                    all_sprites.draw(screen)
                if self.show_board[y][x] == 'F':
                    all_sprites = pygame.sprite.Group()
                    sprite = pygame.sprite.Sprite()
                    sprite.image = load_image("flag.png", transform=True)
                    sprite.rect = sprite.image.get_rect()
                    all_sprites.add(sprite)
                    sprite.rect.x = self.left + x * self.cell_size + 10
                    sprite.rect.y = self.top + y * self.cell_size + 10
                    all_sprites.draw(screen)
                if self.show_board[y][x].isdigit() and \
                    self.show_board[y][x] != '0':
                    self.text_number(self.show_board[y][x],
                              self.left + x * self.cell_size + 15,
                              self.top + y * self.cell_size + 10)
        self.text(check_win(self.show_board))

    def get_click(self, mouse_pos, turn):
        cell = self.get_cell(mouse_pos)
        if turn == 'open':
            self.on_click(cell)
        elif turn == 'flag':
            self.do_flag(cell)
        if check_win(self.show_board):
            self.game_status = False
            self.text(check_win(self.show_board))


    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x not in range(0, 6) or cell_y not in range(0, 6):
            return None
        return (cell_y, cell_x)

    def on_click(self, cell_coords):
        if self.game_status:
            if 0 <= cell_coords[0] < 6 and 0 <= cell_coords[1] < 6:
                if self.board[cell_coords[0]][cell_coords[1]] == '':
                    self.show_board[cell_coords[0]][cell_coords[1]] = '   '

                    self.board[cell_coords[0]][cell_coords[1]] = '[*]'
                    self.on_click((cell_coords[0] - 1, cell_coords[1]))
                    self.on_click((cell_coords[0], cell_coords[1] - 1))
                    self.on_click((cell_coords[0], cell_coords[1] + 1))
                    self.on_click((cell_coords[0] + 1, cell_coords[1]))
                else:
                    if self.board[cell_coords[0]][cell_coords[1]].isdigit():
                        self.show_board[cell_coords[0]][cell_coords[1]] = \
                            self.board[cell_coords[0]][cell_coords[1]]
                    elif self.board[cell_coords[0]][cell_coords[1]] == 'b':
                        self.show_board[cell_coords[0]][cell_coords[1]] = 'boom'
                        print(self.show_board)
                        self.game_status = False
    def do_flag(self, cell_coords):
        if self.game_status:
            if 0 <= cell_coords[0] < 6 and 0 <= cell_coords[1] < 6:
                    self.show_board[cell_coords[0]][cell_coords[1]] = 'F'


    def place_number(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 'b':
                    count = 0
                    if 0 <= i - 1 < 6 and 0 <= j - 1 < 6 and \
                        self.board[i - 1][j - 1] == 'b':
                        count += 1
                    if 0 <= i - 1 < 6 and 0 <= j < 6 and \
                        self.board[i - 1][j] == 'b':
                        count += 1
                    if 0 <= i - 1 < 6 and 0 <= j + 1 < 6 and \
                        self.board[i - 1][j + 1] == 'b':
                        count += 1
                    if 0 <= i < 6 and 0 <= j - 1 < 6 and \
                        self.board[i][j - 1] == 'b':
                        count += 1
                    if 0 <= i < 6 and 0 <= j + 1 < 6 and \
                        self.board[i][j + 1] == 'b':
                        count += 1
                    if 0 <= i + 1 < 6 and 0 <= j - 1 < 6 and \
                        self.board[i + 1][j - 1] == 'b':
                        count += 1
                    if 0 <= i + 1 < 6 and 0 <= j < 6 and \
                        self.board[i + 1][j] == 'b':
                        count += 1
                    if 0 <= i + 1 < 6 and 0 <= j + 1 < 6 and \
                        self.board[i + 1][j + 1] == 'b':
                        count += 1
                    if count != 0:
                        self.board[i][j] = str(count)


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
        rect=pygame.Rect((60, 0), (400, 200)),
        manager=manager,
        window_title='Правила',
        html_message='<font color="black">Ваша цель открыть всё поле, не наступив на бомбу. Левая кнопка мыши открывает клетку, правая - ставит флаг.'
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
    board = Board(6, 6)
    board.set_view(150, 50, 45)
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
                    if event.button == 1:
                        board.get_click(event.pos, 'open')
                    elif event.button == 3:
                        board.get_click(event.pos, 'flag')
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