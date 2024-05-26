import pygame
import itertools


class Math:
    """
    Класс, предназначенный для собственных математических функций
    """
    @staticmethod
    def clamp(value, minm, maxm):
        """
        Удерживает значение value в отрезке [minm, maxm]
        """
        return max(minm, min(value, maxm))

    @staticmethod
    def fix_precision(value):
        """
        Округляет числа с плавающей точкой до x.x
        """
        return round(value, 1)


class Settings:
    """
    Статический класс с настройками игры
    """
    screen_width = 800
    screen_height = 600

    tile_size = 10
    tiles_max_x = 80
    tiles_max_y = 60

    @staticmethod
    def get_map_size():
        """
        Возвращает размер карты
        """
        return (
            Settings.tile_size * Settings.tiles_max_x,
            Settings.tile_size * Settings.tiles_max_y
        )

    @staticmethod
    def get_screen_center():
        """
        Возвращает координаты центра экрана
        """
        return (
                Settings.screen_width // 2,
                Settings.screen_height // 2
            )

    def __init__(self):
        raise AttributeError("Attempt to initialize an abstract class")


class Camera:
    """
    Класс, отвечающий за расположение и размер рисуемых объектов
    """
    zoom = 1.0
    offset = [0, 0]

    def render(self, screen, func):
        """
        Отрисовывает на экране функцию со смещением и отдалением
        """
        func(screen, self.zoom, self.offset)

    def translate(self, position):
        """
        Переносит координаты в зависимости от положения камеры в мире
        и отдаления
        """
        return (
            (position[0] - self.offset[0]) * self.zoom,
            (position[1] - self.offset[1]) * self.zoom)

    def translate_rect(self, rect):
        """
        Переносит координаты и размер в зависимости от положения камеры в мире
        и отдаления
        """
        return (
            (rect[0] - self.offset[0]) * self.zoom,
            (rect[1] - self.offset[1]) * self.zoom,
            rect[2] * self.zoom,
            rect[3] * self.zoom
            )

    def get_tile_id_for_pos(self, pos):
        """
        Возвращает номер клетки, ближайшей к данным координатам
        """
        world_center = self.translate(Settings.get_screen_center())
        center_relative_pos = (
            pos[0] * self.zoom - world_center[0],
            pos[1] * self.zoom - world_center[1]
        )
        return (
            int(center_relative_pos[0] // (Settings.tile_size * self.zoom)
                + Settings.tiles_max_x // 2),
            int(center_relative_pos[1] // (Settings.tile_size * self.zoom)
                + Settings.tiles_max_y // 2)
        )

    def get_pos_for_tile_id(self, x, y):
        """
        Возвращает положение клетки на экране
        """
        world_center = self.translate(Settings.get_screen_center())
        return (
            ((x - (Settings.tiles_max_x // 2))
                * (Settings.tile_size) + world_center[0])
            * camera.zoom,
            ((y - (Settings.tiles_max_y // 2))
                * (Settings.tile_size) + world_center[1])
            * camera.zoom
        )


class GameMap():
    """
    Класс, отвечающий за взаимодействие с игровым полем
    """
    __tiles = [
        [0 for _ in range(Settings.tiles_max_x)]
        for _ in range(Settings.tiles_max_y)
    ]
    __old_tiles = None

    def count_neighbours(self, x, y, old=True):
        """
        Высчитывает количество соседей данной клетки
        """
        count = 0
        if old:
            get_tile = self.get_old_tile
        else:
            get_tile = self.get_tile
        for i in itertools.product([-1, 0, 1], repeat=2):
            if i == (0, 0):
                continue
            count += get_tile(x + i[0], y + i[1])
        return count

    def set_tile(self, x, y, value):
        """
        Устанавливает значение клетки
        """
        if x < 0 or x > Settings.tiles_max_x - 1:
            return
        if y < 0 or y > Settings.tiles_max_y - 1:
            return
        self.__tiles[y][x] = value

    def get_tile(self, x, y):
        """
        Возвращает значение клетки
        """
        if x < 0 or x > Settings.tiles_max_x - 1:
            return 0
        if y < 0 or y > Settings.tiles_max_y - 1:
            return 0
        return self.__tiles[y][x]

    def get_old_tile(self, x, y):
        """
        Возвращает значение клетки в прошлом поколении
        """
        if x < 0 or x > Settings.tiles_max_x - 1:
            return 0
        if y < 0 or y > Settings.tiles_max_y - 1:
            return 0
        return self.__old_tiles[y][x]

    def next_gen(self):
        """
        Проводит процесс "развития":
        сохраняет текущее поколение и создаёт новое
        """
        self.__old_tiles = [[x for x in y] for y in self.__tiles]
        for y in range(Settings.tiles_max_y):
            for x in range(Settings.tiles_max_x):
                neighbours = game_map.count_neighbours(x, y)
                if game_map.get_old_tile(x, y) == 0 and neighbours == 3:
                    game_map.set_tile(x, y, 1)
                elif (game_map.get_old_tile(x, y) == 1
                        and neighbours not in [2, 3]):
                    game_map.set_tile(x, y, 0)

    def get_all_tiles(self):
        """
        Возвращает список всех клеток
        """
        return self.__tiles

    def __init__(self):
        pass


pygame.init()
screen = pygame.display.set_mode(
    (Settings.screen_width, Settings.screen_height)
    )
clock = pygame.time.Clock()
camera = Camera()

game_map = GameMap()


def draw_grid(surface, scale, offset):
    """
    Для упрощения отрисовки фона, мы разбили его на несколько частей
    Данная функция отрисовывает клетки, которые помещаются на экране
    """
    surface.fill("white")
    curX = 0
    while curX <= Settings.screen_width:
        pygame.draw.line(
            surface, "black",
            (curX, 0),
            (curX, Settings.screen_height))
        curX += Settings.tile_size * scale
    curY = 0
    while curY <= Settings.screen_height:
        pygame.draw.line(
            surface, "black",
            (0, curY),
            (Settings.screen_width, curY))
        curY += Settings.tile_size * scale


def create_background(surface, scale, offset):
    """
    Данная функция собирает из ранее отрисованного изображения фон
    """
    grid = pygame.Surface(
        (Settings.screen_width, Settings.screen_height))
    draw_grid(grid, scale, offset)

    y = 0
    while y < Settings.get_map_size()[1]:
        x = 0
        while x < Settings.get_map_size()[0]:
            surface.blit(grid, (x, y))
            x += Settings.screen_width
        y += Settings.screen_height


background = pygame.Surface(
        Settings.get_map_size()
    )

create_background(background, 1, (0, 0))

run = True

drag = False
drag_start_pos = None

draw = False
draw_erase = False
draw_start_pos = None

simulate = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Выход
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # ЛКМ
                if pygame.key.get_mods() & pygame.KMOD_CTRL:  # Если зажат любой Ctrl
                    draw_erase = True  # Переходим в режим удаления
                else:
                    draw_erase = False
                draw_start_pos = event.pos
                draw = True
                tile_id = camera.get_tile_id_for_pos(event.pos)
                if game_map.get_tile(*tile_id) > 0:
                    game_map.set_tile(tile_id[0], tile_id[1], 0)
                else:
                    game_map.set_tile(tile_id[0], tile_id[1], 1)
            if event.button == 3:  # ПКМ
                drag_start_pos = event.pos
                drag = True  # Включаем передвижение камерой
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                draw = False
            if event.button == 3:
                drag = False
        if event.type == pygame.MOUSEMOTION:
            if draw:
                tile_id = camera.get_tile_id_for_pos(event.pos)
                if draw_erase:
                    game_map.set_tile(tile_id[0], tile_id[1], 0)
                else:
                    game_map.set_tile(tile_id[0], tile_id[1], 1)
            if drag:
                camera.offset = \
                    [
                        Math.clamp(
                            camera.offset[x] - event.rel[x],
                            -Settings.get_map_size()[x]//2,
                            Settings.get_map_size()[x]//2
                        )
                        for x in range(2)
                    ]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:  # Запускаем/Останавливаем симуляцию по нажатию пробела
                simulate = not simulate

    if simulate:
        game_map.next_gen()

    # Рисуем фон
    screen.fill("white")
    screen.blit(
        background,
        camera.translate((
            0,
            0
        ))
    )

    # Отрисовываем закрашенные клетки
    x = 0
    while x < Settings.screen_width:
        y = 0
        while y < Settings.screen_height:
            tile_id = camera.get_tile_id_for_pos((x, y))
            pos = camera.get_pos_for_tile_id(*tile_id)
            if game_map.get_tile(*tile_id) > 0:
                pygame.draw.rect(
                    screen,
                    "black",
                    pos +
                    (
                        Settings.tile_size * camera.zoom,
                        Settings.tile_size * camera.zoom
                    )
                )
            y += Settings.tile_size * camera.zoom
        x += Settings.tile_size * camera.zoom

    pygame.display.flip()
    clock.tick(60)  # 60 FPS


pygame.quit()
