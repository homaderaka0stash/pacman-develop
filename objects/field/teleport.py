from objects.field.tile import Tile


class Teleport(Tile):
    def __init__(self, x: int, y: int, direction, tele_pair_x, tele_pair_y):
        super().__init__(x, y)
        self.direction = direction
        self.tele_pair_x = tele_pair_x
        self.tele_pair_y = tele_pair_y

    def get_direction(self):
        return self.direction

    def get_pair_teleport(self):
        return self.tele_pair_x, self.tele_pair_y
