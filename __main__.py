import pygame


class Math:
    @staticmethod
    def clamp(value, minm, maxm):
        return max(minm, min(value, maxm))

    def fix_precision(value):
        return round(value, 1)


class Settings:
    screen_width = 800
    screen_height = 600

    tile_size = 10
    tiles_max_x = 1250
    tiles_max_y = 1250

    @staticmethod
    def get_screen_center():
        return (
                Settings.screen_width // 2,
                Settings.screen_height // 2
            )

    def __init__(self):
        raise AttributeError("Attempt to initialize an abstract class")


class Camera:
    zoom = 1.0
    offset = [0, 0]

    def render(self, screen, func):
        func(screen, self.zoom, self.offset)

    def translate(self, position):
        return (
            (position[0] - self.offset[0]) * self.zoom,
            (position[1] - self.offset[1]) * self.zoom)

    def translate_rect(self, rect):
        return (
            (rect[0] - self.offset[0]) * self.zoom,
            (rect[1] - self.offset[1]) * self.zoom,
            rect[2] * self.zoom,
            rect[3] * self.zoom
            )

    def get_tile_id_for_pos(self, pos):
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
        world_center = self.translate(Settings.get_screen_center())
        return (
            ((x - (Settings.tiles_max_x // 2))
                * (Settings.tile_size * self.zoom) + world_center[0])
            * camera.zoom,
            ((y - (Settings.tiles_max_y // 2))
                * (Settings.tile_size * self.zoom) + world_center[1])
            * camera.zoom
        )


class GameMap():
    __tiles = [
        [0 for x in range(Settings.tiles_max_x)]
        for y in range(Settings.tiles_max_y)
        ]

    def count_neighbours(self, x, y):
        return self.count_neighbours()

    def set_tile(self, x, y, value):
        self.__tiles[y][x] = value

    def get_tile(self, x, y):
        return self.__tiles[y][x]

    def get_all_tiles(self):
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


def drawBackground(screen, scale, offset):
    curX = 0
    while curX <= Settings.screen_width:
        pygame.draw.line(
            screen, "black",
            camera.translate((curX, 0)),
            camera.translate((curX, Settings.screen_height)))
        curX += Settings.tile_size * camera.zoom
    curY = 0
    while curY <= Settings.screen_height:
        pygame.draw.line(
            screen, "black",
            camera.translate((0, curY)),
            camera.translate((Settings.screen_width, curY)))
        curY += Settings.tile_size * camera.zoom


run = True

drag = False
drag_start_pos = None

draw = False
draw_start_pos = None

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            camera.zoom = Math.fix_precision(Math.clamp(
                camera.zoom + event.precise_y / 10, 1, 1))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (event.button == 1):
                draw_start_pos = event.pos
                draw = True
                tile_id = camera.get_tile_id_for_pos(event.pos)
                if game_map.get_tile(*tile_id) > 0:
                    game_map.set_tile(tile_id[0], tile_id[1], 0)
                else:
                    game_map.set_tile(tile_id[0], tile_id[1], 1)
            if (event.button == 3):
                drag_start_pos = event.pos
                drag = True
        if event.type == pygame.MOUSEBUTTONUP:
            if (event.button == 1):
                draw = False
            if (event.button == 3):
                drag = False
        if event.type == pygame.MOUSEMOTION:
            if draw:
                tile_id = camera.get_tile_id_for_pos(event.pos)
                game_map.set_tile(tile_id[0], tile_id[1], 1)
            if drag:
                camera.offset = \
                    [camera.offset[x] - event.rel[x] for x in range(2)]

    screen.fill("white")
    camera.render(screen, drawBackground)

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
            y += Settings.tile_size * camera.zoom / 2
        x += Settings.tile_size * camera.zoom / 2

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
