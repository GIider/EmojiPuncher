# coding=utf-8
import os

from .effect import Blam
from .enemy import Enemy
from .entity import TimedEntity
from ..constant import Direction, IMAGE_FOLDER

__all__ = ['Punch']


class Punch(TimedEntity):
    time_alive = 85
    damage = 1

    punch_images = {Direction.LEFT: os.path.join(IMAGE_FOLDER, 'punch', '1f91b.png'),
                    Direction.RIGHT: os.path.join(IMAGE_FOLDER, 'punch', '1f91c.png')}

    def __init__(self, game, player, direction):
        super().__init__(game)

        self.player = player
        self.direction = direction
        self.hit_enemies = []

        self.load_sprite(path=self.punch_images[direction])
        self.load_position()

    def load_position(self):
        if self.direction == Direction.RIGHT:
            self.x = self.player.x + self.width
        elif self.direction == Direction.LEFT:
            self.x = self.player.x - self.width

        self.y = self.player.y

    def update(self, time_passed):
        super(Punch, self).update(time_passed)

        for entity in self.game.entities:
            if isinstance(entity, Enemy) and self.colliding(entity) and entity not in self.hit_enemies:
                self.punch_enemy(enemy=entity)

    def punch_enemy(self, enemy):
        enemy.hurt(damage=self.damage)
        self.hit_enemies.append(enemy)

        Blam.spawn(game=self.game, enemy=enemy)
