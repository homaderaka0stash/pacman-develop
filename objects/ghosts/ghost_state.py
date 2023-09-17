import enum


class GhostState(enum.Enum):
    is_dead = 0
    is_moving = 1
    is_stop = 2
