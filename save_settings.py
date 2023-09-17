import os

from main_settings import field_height, field_width
from objects.field.collectible.bonus import Bonus
from objects.field.collectible.food import Food
from objects.field.teleport import Teleport
from objects.field.tile import Tile
from objects.field.wall import Wall
from main_settings import save_ghost_path, save_score_path


class Save:
    def __init__(self, save_map_path, save_pacman_position=None, save_blinky_position=None, save_pinky_position=None, save_inky_position=None, save_clyde_position=None, score=None, lives=None):
        self.save_blinky_position = save_blinky_position
        self.save_pinky_position = save_pinky_position
        self.save_inky_position = save_inky_position
        self.save_clyde_position = save_clyde_position
        self.score = score
        self.lives = lives
        self.save_map_path = save_map_path
        self.start_pacman_position = save_pacman_position

    def create_save_map(self, save_field):
        with open(self.save_map_path, 'w') as f:
            save_ext_tile = []
            for i in range(field_height):
                for j in range(field_width):
                    if isinstance(save_field[i][j], Wall):
                        f.write(str(save_field[i][j].type) + " ")
                    elif isinstance(save_field[i][j], Food):
                        f.write("+" + " ")
                    elif isinstance(save_field[i][j], Bonus):
                        f.write("O" + " ")
                    elif isinstance(save_field[i][j], Teleport):
                        f.write("." + " ")
                        save_ext_tile.append(list(("Teleport", list((i, j)))))
                    elif isinstance(save_field[i][j], Tile):
                        f.write("." + " ")
                f.write("\n")

            for i in range(len(save_ext_tile)):
                f.write(save_ext_tile[i][0] + " " + str(save_ext_tile[i][1][1]) + " " + str(save_ext_tile[i][1][0])
                        + " " + save_field[save_ext_tile[i][1][0]][save_ext_tile[i][1][1]].direction + " " +
                        str(save_field[save_ext_tile[i][1][0]][save_ext_tile[i][1][1]].tele_pair_x) + " " +
                        str(save_field[save_ext_tile[i][1][0]][save_ext_tile[i][1][1]].tele_pair_y) + " " +
                        save_field[save_field[save_ext_tile[i][1][0]][save_ext_tile[i][1][1]].tele_pair_y][
                            save_field[save_ext_tile[i][1][0]][save_ext_tile[i][1][1]].tele_pair_x].direction + "\n")

            f.write("Pacman_position" + " " + str(self.start_pacman_position[0])
                    + " " + str(self.start_pacman_position[1]) + "\n")
            self.save_ghosts()
            self.save_score()

    def save_score(self):
        with open(save_score_path, 'w') as f:
            f.write(str(self.score) + " " + str(self.lives))

    def save_ghosts(self):
        with open(save_ghost_path, 'w') as f:
            f.write(str(self.save_blinky_position[0]) + " " + str(self.save_blinky_position[1]) + "\n" + str(
                self.save_pinky_position[0]) + " " + str(self.save_pinky_position[1]) + "\n" + str(
                self.save_inky_position[0]) + " " + str(self.save_inky_position[1]) + "\n" + str(
                self.save_clyde_position[0]) + " " + str(self.save_clyde_position[1]))

    def delete_save_map(self):
        if os.path.exists(self.save_map_path):
            os.remove(self.save_map_path)
        if os.path.exists(save_ghost_path):
            os.remove(save_ghost_path)
        if os.path.exists(save_score_path):
            os.remove(save_score_path)
