# coding=utf-8
import enum

import pygame
import os


class Direction(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    @classmethod
    def from_key(cls, key):
        return ASSIGNED_KEY[key]


DIRECTION_KEYS = (pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN)
PUNCHING_KEYS = (pygame.K_a, pygame.K_d)

IMAGE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

ASSIGNED_KEY = {pygame.K_LEFT: Direction.LEFT,
                pygame.K_RIGHT: Direction.RIGHT,
                pygame.K_DOWN: Direction.DOWN,
                pygame.K_UP: Direction.UP,

                pygame.K_a: Direction.LEFT,
                pygame.K_d: Direction.RIGHT}
