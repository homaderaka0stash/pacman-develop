from pygame.surface import Surface

from objects.field.collectible.bonus import Bonus
from objects.field.collectible.food import Food
from objects.field.dev_easter_eggs.roma_state.collectible.chest import Chest
from objects.field.dev_easter_eggs.roma_state.collectible.ice_cream import Ice_cream
from objects.field.dev_easter_eggs.roma_state.collectible.super_coin import Super_coin
from objects.field.dev_easter_eggs.roma_state.destructible_wall import Destructible_wall
from objects.field.dev_easter_eggs.roma_state.none_tile import None_tile
from objects.field.teleport import Teleport
from objects.field.tile import Tile
from objects.field.wall import Wall
from settings import pixel_tile


class Field:
    def __init__(self, map_path, field_width, field_height):
        self.field_width = field_width
        self.field_height = field_height
        self.map_path = map_path
        self.food_count = 0

        self.field = [list()] * field_height
        for i in range(field_height):
            self.field[i] = [Tile] * field_width

        self.field_turn = [list()] * field_height
        for i in range(field_height):
            self.field_turn[i] = [False] * field_width

        self.map_load()
        self.set_walls()

    def map_load(self):
        try:
            with open(self.map_path, 'r') as f:
                for i in range(self.field_height):
                    map_str = list(f.readline().strip().split())
                    for j in range(self.field_width):
                        if map_str[j].isdigit():
                            self.field[i][j] = Wall(j * pixel_tile, i * pixel_tile, int(map_str[j]))
                        elif map_str[j] == "D":
                            self.field[i][j] = Destructible_wall(j * pixel_tile, i * pixel_tile, 1)
                        elif map_str[j] == "d":
                            self.field[i][j] = Destructible_wall(j * pixel_tile, i * pixel_tile, 2)
                        elif map_str[j] == "+":
                            self.field[i][j] = Food(j * pixel_tile, i * pixel_tile)
                            self.food_count += 1
                        elif map_str[j] == "O":
                            self.field[i][j] = Bonus(j * pixel_tile, i * pixel_tile)
                        elif map_str[j] == "F":
                            self.field[i][j] = Super_coin(j * pixel_tile, i * pixel_tile)
                        elif map_str[j] == "I":
                            self.field[i][j] = Chest(j * pixel_tile, i * pixel_tile)
                        elif map_str[j] == "L":
                            self.field[i][j] = Ice_cream(j * pixel_tile, i * pixel_tile)
                        elif map_str[j] == "*":
                            self.field[i][j] = None_tile(j * pixel_tile, i * pixel_tile)
                        else:
                            self.field[i][j] = Tile(j * pixel_tile, i * pixel_tile)
                while True:
                    tile_type_str = list(f.readline().strip().split())
                    if tile_type_str == "":
                        break
                    if tile_type_str[0] == "Teleport":
                        i = int(tile_type_str[1])
                        j = int(tile_type_str[2])
                        direction_1 = tile_type_str[3]
                        ii = int(tile_type_str[4])
                        jj = int(tile_type_str[5])
                        direction_2 = tile_type_str[6]
                        self.field[j][i] = Teleport(i * pixel_tile, j * pixel_tile, direction_1, ii, jj)
                        self.field[jj][ii] = Teleport(ii * pixel_tile, jj * pixel_tile, direction_2, i, j)

                    elif tile_type_str[0] == "Turn":
                        for _ in range(int(tile_type_str[1])):
                            tile_type = list(f.readline().strip().split())
                            self.field_turn[int(tile_type[1])][int(tile_type[0])] = True

        except Exception as e:
            print(e)

    def set_walls(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                if isinstance(self.field[i][j], Wall):
                    if 1 == self.field[i][j].type:
                        if i > 0:
                            if isinstance(self.field[i - 1][j], Wall):
                                self.field[i][j].sections[0][1] = True
                        if i < self.field_height - 1:
                            if isinstance(self.field[i + 1][j], Wall):
                                self.field[i][j].sections[2][1] = True
                        if j > 0:
                            if isinstance(self.field[i][j - 1], Wall):
                                self.field[i][j].sections[1][0] = True
                        if j < self.field_width - 1:
                            if isinstance(self.field[i][j + 1], Wall):
                                self.field[i][j].sections[1][2] = True
                    elif 2 == self.field[i][j].type:
                        self.field[i][j].sections[1][0], self.field[i][j].sections[1][2] = True, True
                    elif 3 == self.field[i][j].type:
                        self.field[i][j].sections[0][1], self.field[i][j].sections[2][1] = True, True
                    elif 4 == self.field[i][j].type:
                        self.field[i][j].sections[1][0], self.field[i][j].sections[2][1] = True, True
                    elif 5 == self.field[i][j].type:
                        self.field[i][j].sections[1][2], self.field[i][j].sections[2][1] = True, True
                    elif 6 == self.field[i][j].type:
                        self.field[i][j].sections[0][1], self.field[i][j].sections[1][2] = True, True
                    elif 7 == self.field[i][j].type:
                        self.field[i][j].sections[0][1], self.field[i][j].sections[1][0] = True, True

    def process_draw(self, screen: Surface):
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.field[i][j].process_draw(screen)

    def process_tele_draw(self, screen: Surface):
        for i in range(self.field_height):
            for j in range(self.field_width):
                if isinstance(self.field[i][j], Teleport):
                    self.field[i][j].process_draw(screen)
