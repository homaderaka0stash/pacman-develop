from objects.field.tile import Tile


class Collectible(Tile):

    def process_collection(self, field_map):
        field_map[self.rect.y // 21][self.rect.x // 21] = Tile(self.rect.x, self.rect.y)
