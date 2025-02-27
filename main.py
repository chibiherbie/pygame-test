import pygame
from network import Network


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 480, 480
FPS = 30
TILE_SIZE = 32


class Labyrinth:
    def __init__(self, filename, free_tiles, finish_tile):
        self.map = []
        with open(f'{filename}') as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        color = {0: (0, 0, 0), 1: (120, 120, 120), 2:(50, 50, 50)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(color[self.get_tile_id((x, y))], rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


class Hero:
    def __init__(self, position, color):
        self.x, self.y = position
        self.color = pygame.Color(str(color))

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, self.color, center, TILE_SIZE // 2)


class Game:
    def __init__(self, labyrinth, hero1, hero2):
        self.labyrinth = labyrinth
        self.hero1 = hero1
        self.hero2 = hero2

    def render(self, screen):
        self.labyrinth.render(screen)
        self.hero1.render(screen)
        self.hero2.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero1.get_position()
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_w]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_s]:
            next_y += 1

        if self.labyrinth.is_free((next_x, next_y)):
            self.hero1.set_position((next_x, next_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Лабиринт")

    n = Network()

    p1 = n.getP()
    print(p1)

    labyrinth = Labyrinth('simple_map.txt', [0, 2], 2)

    clock = pygame.time.Clock()
    running = True
    while running:
        p2 = n.send(p1)

        game = Game(labyrinth, p1, p2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update_hero()

        game.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
