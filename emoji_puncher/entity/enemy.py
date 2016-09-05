# coding=utf-8
import os
import random

from .entity import Entity
from ..constant import IMAGE_FOLDER

__all__ = ['Enemy']


class Enemy(Entity):
    speed = 0
    sprite_path = os.path.join(IMAGE_FOLDER, 'enemy', '3.png')

    def __init__(self, game, spawner):
        super().__init__(game)

        self.spawner = spawner
        self.hp = 3
        self.speed = random.uniform(0, 0.25)

        self.x = random.choice([0, game.WIDTH])
        self.y = random.randrange(0, game.HEIGHT - self.height)

        if self.x == 0:
            self.x_velocity = self.speed
        else:
            self.x_velocity -= self.speed

    def hurt(self):
        self.hp -= 1

        if self.hp == 0:
            return self.destroy()

        new_sprite_path = os.path.join(IMAGE_FOLDER, 'enemy', '%d.png' % self.hp)
        self.load_sprite(path=new_sprite_path)

    def update(self, time_passed):
        super(Enemy, self).update(time_passed)

        if self.x >= self.game.WIDTH or self.x <= 0:
            self.destroy()

    def destroy(self):
        super(Enemy, self).destroy()

        self.spawner.killed(self)
