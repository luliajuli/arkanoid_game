import pygame

pygame.init()

# класс Area
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Lable(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename).convert_alpha()  # Преобразование в формат с альфа-каналом
        self.remove_white_bg()  # Удаление белого фона

    def remove_white_bg(self):
        color = (255, 255, 255)  # Белый цвет фона

        # Проходим по всем пикселям изображения и заменяем белый на прозрачный
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y))[:3] == color:
                    self.image.set_at((x, y), (255, 255, 255, 0))  # Прозрачный пиксель

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


back = (200, 255, 255)  # цвет сцены
mw = pygame.display.set_mode((500, 500))  # окно программы
mw.fill(back)
clock = pygame.time.Clock()
# координаты платформы
racket_x = 200
racket_y = 330
speed_x = 3
speed_y = 3
# координаты мяча
dx = 3
dy = 3
# флаг окончания игры
game_over = False
win = False

# создание мяча
ball = Picture('ball.png', 160, 200, 50, 50)
# создание платформы
platform = Picture('platform.png', racket_x, racket_y, 100, 30)
# координаты создания первого монстра
start_x = 5
start_y = 5
move_right = False
move_left = False
# список хранения объектов монстров
monsters = []

# количество монстров в каждом ряду
count = [9, 8, 7]

# цикл по строкам
for j in range(3):
    y = start_y + (55 * j)
    x = start_x
    # цикл по столбцам
    for i in range(count[j]):
        d = Picture('enemy.png', x, y, 50, 50)
        monsters.append(d)  # добавление в список монстров
        x += 55  # увеличение координаты следующего монстра


while not game_over:
    ball.fill()
    platform.fill()
    # обработка событий на клавиши
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_LEFT:
                move_left = False

    # Перемещение платформы, если не выходит за пределы окна
    if move_right and platform.rect.x + platform.rect.width < 500:
        platform.rect.x += 3
    elif move_left and platform.rect.x > 0:
        platform.rect.x -= 3

    # Проверка столкновений с краями сцены и изменение направления мяча
    if ball.rect.x <= 0 or ball.rect.x + ball.rect.width >= 500:
        dx *= -1
    if ball.rect.y <= 0:
        dy *= -1

    if ball.rect.y + ball.rect.height >= platform.rect.y + platform.rect.height:
        # Если мяч падает за пределы платформы, игра заканчивается
        game_over = True
        win = False

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.colliderect(platform.rect):
        dy *= -1
    for n in monsters:
        n.draw()
        # удаление монстра из списка, когда касается мяч
        if n.rect.colliderect(ball.rect):
            monsters.remove(n)
            n.fill()
            dy *= -1

    if not monsters:  # Если список монстров пуст, игрок выиграл
        game_over = True
        win = True

    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)

# Отображение выигрыша или проигрыша
result_label = Lable(150, 200, 200, 100)
result_label.set_text("YOU WIN!" if win else "YOU LOST!", 40, (255, 0, 0))
result_label.draw()

pygame.display.update()
pygame.time.wait(2000)  # Пауза перед завершением игры
