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
winner = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Snow(pygame.sprite.Sprite):#осноовная картинка
    image = load_image("moun.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Snow.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


mountain = Snow()
y_pos = 215#координаты у
my = []
count = 0
y_p = 0
xx = 0
yy = 0
st = 0
counter = 0
a = []#список для координат
font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("arial", 35)
flag_of_game = True
blocked = False


def message(msg, color):#передает и вывод сообщение
    mess = font_style.render(msg, True, color)
    screen.blit(mess, [200, 225])


def show_message_above_field():#получает и вывод сообщение

    global width, screen

    if winner:
        message = 'Вы победили'
    else:
        message = 'Вы проиграли'

    pygame.draw.rect(screen, 'black', (60, 0, 400, 50))

    font = pygame.font.Font(None, 50)
    string_rendered = font.render(message, True, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
    screen.blit(string_rendered, intro_rect)


class Landing(pygame.sprite.Sprite):
    image = load_image("kvadrat.png")#сама фигурка

    def __init__(self, pos):
        global my, y_pos, count, result, y_p, st, a, counter
        super().__init__(all_sprites)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        counter += 1
        st += 1
        if st != 1:
            xx = self.rect.x
            yy = self.rect.y
        if result % 2 == 0 and count != 1:
            a += [self.rect.x, self.rect.y]#добавление координат в список
            count += 1
            if count != 1:
                y_pos -= 25

    def show_message(self, message, font_size=50):
        global width, screen
        font = pygame.font.Font(None, font_size)
        string_rendered = font.render(message, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x, intro_rect.y = width // 2 - intro_rect.width // 2, 10
        screen.blit(string_rendered, intro_rect)

    def update(self):

        global current_block_id

        try:
            global y_pos, count, result, my, y_p, flag_of_adding, flag_of_game, blocked, winner, should_show_message
            count += 1
            if blocked:
                return

            if result % 2 != 0 and id(self) == current_block_id:#блок перемещается из стороны в сторону
                self.rect.x += 5
                if self.rect.left > width:
                    self.rect.right = 0
            else:#блок нчинает падать
                if not pygame.sprite.collide_mask(self, mountain) and self.rect.y < y_pos:
                    self.rect = self.rect.move(0, 5)
                if self.rect.y == y_pos:
                    my += [self.rect.x, self.rect.y]
                    current_block_id = id(Landing([122, 10]))#загружается новый блок
                    y_p += 1
                    result += 1
                    count += 1
                if counter == 8:#если достигнуть максимальное колиечство кубиков подряд без ошибок
                    should_show_message = True
                    if not winner:
                        show_rules('Благодаря вам Дед Мороз нашел 1 подарок!')
                    winner = True
                    blocked = True
                if counter != 1 and counter != 2:
                    if abs(int(my[-2]) - int(my[0])) >= 13 or abs(int(my[-2]) - int(my[-4])) >= 13:
                        #если слишком большой сдвиг
                        should_show_message = True
                        blocked = True
                if counter == 2:
                    if abs(int(my[-2]) - int(my[0])) >= 13:
                        #если слишкои большой сдвиг
                        should_show_message = True
                        blocked = True
        except Exception as a:
            print(a)


def show_rules(message=None):#окно с правилами
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
            html_message='<font color="black">Постройте башню, чтобы она не упала. ' + \
                         'Чтобы начать игру, вам нужно нажать мышкой на экран(около крестика например). ' + \
                         'По экрану начнет передвигаться блок, ваша задача - кликнуть на него в такой момент, ' + \
                         'чтобы блок упал на землю с определенными координатами и получилась башенка из кубиков. ' + \
                         'Если вы будете класть кубики неровно - это приведет к проигрышу. ' + \
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


def confirmation_exit_dialog():#окно с выходом из игры
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
    global width, height, screen, manager, confirmation_mini_game_dialog, result, current_block_id, y_p, xx, yy, my, \
        winner, blocked, should_show_message

    width, height = 550, 550
    screen = pygame.display.set_mode((width, height))
    manager = pygame_gui.UIManager((width, height))

    should_show_message = False

    winner, blocked = False, False

    current_block_id = None

    #создание кнопок
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
        screen.fill((255, 255, 255))
        t = clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #описание кнопок
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not (event.pos[0] < 50 and event.pos[1] < 50 or event.pos[0] > 500 and event.pos[
                    1] < 50) and not status_game_blocked:#проверка на границы
                    result += 1
                    if result == 1:
                        current_block_id = id(Landing([122, 10]))
                        y_p += 1
            manager.process_events(event)
        manager.update(60 / 1000)
        if not status_game_blocked:
            all_sprites.update()
        all_sprites.draw(screen)
        if should_show_message:
            show_message_above_field()
        manager.draw_ui(screen)
        pygame.display.flip()

    return winner


if __name__ == '__main__':
    pygame.init()
    main()
