import pygame
import sys
import random

pygame.init()
import pygame_menu

bg_image = pygame.image.load('logo.png')

# Sound
apple_eat = pygame.mixer.Sound('bonus.wav')
lose_sound = pygame.mixer.Sound('game-over.wav')
menu_sound = pygame.mixer.Sound('dreams.mp3')

# Размер блока задаем
SIZE_BLOCK = 20
# Цвет задаем
FRAME_COLOR = (114, 129, 114)
WHITE = (255, 255, 255)
BLUE = (54, 44, 44)
RED = (250, 10, 10)
HEADER_COLOR = (119, 119, 119)
SNAKE_COLOR = (58, 216, 53)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
# Задаем размер окна которое будет у нас
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]
print(size)
#  Задаем окно в котором будет всё происходить
screen = pygame.display.set_mode(size)
# Задаем имя Окна "Змейка"
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 30)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1
    # Задаем бесконечный цикл, что бы окно не закрывалось
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
        # Задаем цвет окна
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f"Total: {total}", 0, WHITE)
        speed_total = courier.render(f"Speed: {speed}", 0, WHITE)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(speed_total, (SIZE_BLOCK + 200, SIZE_BLOCK))

        # Начинаем задавать квадраты для поля
        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (column + row) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE
                    draw_block(color, row, column)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('crash')
            pygame.mixer.Sound.play(lose_sound)
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if apple == head:
            total += 1
            speed = total // 2 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()
            pygame.mixer.Sound.play(apple_eat)

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print('Kill yourself')
            pygame.mixer.Sound.play(lose_sound)
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(4 + speed)

    # def set_difficulty(value, difficulty):
    #     # Do the job here !
    #     pass

main_theme = pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.7)

menu = pygame_menu.Menu('Snake', 220, 300,
                        theme=main_theme)

menu.add.text_input('Name :', default=' ')
# menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
pygame.mixer.Sound.play(menu_sound)
while True:

    screen.blit(bg_image, (80, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

