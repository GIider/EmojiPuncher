# coding=utf-8
import os
import time

from .enemy import Enemy
from .entity import Entity
from ..constant import Direction, IMAGE_FOLDER

__all__ = ['Punch']


class Punch(Entity):
    time_spawned = 0
    time_alive = 0.125

    punch_images = {Direction.LEFT: os.path.join(IMAGE_FOLDER, 'punch', '1f91b.png'),
                    Direction.RIGHT: os.path.join(IMAGE_FOLDER, 'punch', '1f91c.png')}

    def __init__(self, game, player, direction):
        super().__init__(game)

        self.time_spawned = time.time()
        self.player = player
        self.direction = direction
        self.hit_enemies = []

        self.load_sprite(path=self.punch_images[direction])
        self.update()

    @classmethod
    def spawn(cls, player, direction):
        sprite = cls(game=player.game, player=player, direction=direction)
        sprite.game.entities.append(sprite)

        return sprite

    @property
    def expiry_time(self):
        return self.time_spawned + self.time_alive

    def update(self):
        if not self.alive:
            return

        if self.direction == Direction.RIGHT:
            self.x = self.player.x + self.width
        elif self.direction == Direction.LEFT:
            self.x = self.player.x - self.width

        self.y = self.player.y

        for entity in self.game.entities:
            if isinstance(entity, Enemy) and self.colliding(entity) and entity not in self.hit_enemies:
                entity.hurt()
                self.hit_enemies.append(entity)

        now = time.time()
        if now >= self.expiry_time:
            self.destroy()
