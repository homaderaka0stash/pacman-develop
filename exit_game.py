import sys
from save_settings import Save
from main_settings import save_map_path


def exit_game():
    Save(save_map_path, None, None, None, None, None, None, None).delete_save_map()
    sys.exit(0)
