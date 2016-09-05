# coding=utf-8
import os

import pygame

from .entity import TimedEntity
from ..constant import IMAGE_FOLDER

__all__ = ['Blam', 'LevelUp']


class Blam(TimedEntity):
    time_alive = 40

    sprite_path = os.path.join(IMAGE_FOLDER, 'effect', 'blam.png')

    def __init__(self, game, enemy):
        super(Blam, self).__init__(game)

        self.enemy = enemy
        self.load_position()

    @classmethod
    def spawn(cls, enemy):
        sprite = cls(game=enemy.game, enemy=enemy)
        sprite.game.entities.append(sprite)

        return sprite

    def load_position(self):
        self.x = self.enemy.x
        self.y = self.enemy.y

    def update(self, time_passed):
        super(Blam, self).update(time_passed)

        if not self.alive:
            return

        self.sprite = pygame.transform.rotate(self.sprite, 90 * time_passed)


class LevelUp(TimedEntity):
    time_alive = 100

    sprite_path = os.path.join(IMAGE_FOLDER, 'effect', 'levelup.png')

    def __init__(self, game, player):
        super(LevelUp, self).__init__(game)

        self.player = player

    def load_position(self):
        self.x = self.player.x
        self.y = self.player.y + self.height

    def update(self, time_passed):
        super(LevelUp, self).update(time_passed)

        if not self.alive:
            return
