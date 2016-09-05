# coding=utf-8
import os

import pygame

from .entity import Entity
from .punch import Punch
from ..constant import IMAGE_FOLDER, Direction, DIRECTION_KEYS, PUNCHING_KEYS

__all__ = ['Player']


class Player(Entity):
    speed = 0.55
    sprite_path = os.path.join(IMAGE_FOLDER, 'player.png')
    angry_sprite_path = os.path.join(IMAGE_FOLDER, 'player_angry.png')

    def __init__(self, game):
        self.moving = False
        self._punch = None

        super().__init__(game)

    def process_keydown(self, key):
        if key in PUNCHING_KEYS:
            self.punch(direction=Direction.from_key(key=key))

    @property
    def is_punching(self):
        return not (self._punch is None or not self._punch.alive)

    def punch(self, direction):
        if not self.is_punching:
            punch = Punch.spawn(game=self.game, player=self, direction=direction)
        else:
            punch = self._punch

        self._punch = punch

    @property
    def sprite(self):
        if self.is_punching:
            return self.load_sprite(path=self.angry_sprite_path)
        else:
            return self.load_sprite(path=self.sprite_path)

    @sprite.setter
    def sprite(self, value):
        return

    def update(self, time_passed):
        pressed_keys = pygame.key.get_pressed()

        is_moving = False
        for direction_key in DIRECTION_KEYS:
            if pressed_keys[direction_key]:
                direction = Direction.from_key(key=direction_key)
                is_moving = True

                if direction == Direction.LEFT:
                    self.x_velocity -= self.speed
                elif direction == Direction.RIGHT:
                    self.x_velocity += self.speed
                elif direction == Direction.DOWN:
                    self.y_velocity += self.speed
                elif direction == Direction.UP:
                    self.y_velocity -= self.speed

        if not is_moving:
            self.x_velocity = self.x_velocity - min(abs(self.x_velocity), self.friction) * self.x_velocity
            self.y_velocity = self.y_velocity - min(abs(self.y_velocity), self.friction) * self.y_velocity

        self.x_velocity = max(min(self.x_velocity, self.maximum_x_velocity), self.minimum_x_velocity)
        self.y_velocity = max(min(self.y_velocity, self.maximum_y_velocity), self.minimum_y_velocity)

        if self.x_velocity == 0 and self.y_velocity == 0:
            self.moving = False

        self.x += self.x_velocity
        self.y += self.y_velocity

        self.x = min(max(self.x + self.x_velocity, 0), self.game.playable_width - self.width)
        self.y = min(max(self.y + self.y_velocity, 0), self.game.playable_height - self.height)
