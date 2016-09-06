# coding=utf-8
import enum
from collections import namedtuple

Size = namedtuple('Size', ('width', 'height'))

GAME_SIZE = Size(800, 400)
TILE_SIZE = Size(64, 64)


class Direction(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
