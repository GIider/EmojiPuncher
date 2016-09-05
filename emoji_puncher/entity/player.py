# coding=utf-8
import os

from .entity import Entity
from .punch import Punch
from ..constant import IMAGE_FOLDER, Direction

__all__ = ['Player']


class Player(Entity):
    speed = 10
    sprite_path = os.path.join(IMAGE_FOLDER, 'player.png')

    def __init__(self, game):
        super().__init__(game)

        self._punch = None

    def punch(self, direction):
        if self._punch is None or not self._punch.alive:
            punch = Punch.spawn(player=self, direction=direction)
        else:
            punch = self._punch

        self._punch = punch

    def move(self, direction):
        if direction == Direction.LEFT:
            self.x_velocity -= self.speed
        elif direction == Direction.RIGHT:
            self.x_velocity += self.speed
        elif direction == Direction.DOWN:
            self.y_velocity += self.speed
        elif direction == Direction.UP:
            self.y_velocity -= self.speed
        else:
            raise ValueError(direction)

    def stop(self, direction):
        if direction == Direction.LEFT:
            self.x_velocity = 0
        elif direction == Direction.RIGHT:
            self.x_velocity = 0
        elif direction == Direction.DOWN:
            self.y_velocity = 0
        elif direction == Direction.UP:
            self.y_velocity = 0
        else:
            raise ValueError(direction)
