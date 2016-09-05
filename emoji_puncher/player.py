# coding=utf-8
import time
import os

import pygame

from .constant import Direction, IMAGE_FOLDER


class Entity(object):
    width = 64
    height = 64

    x = 0
    y = 0

    x_velocity = 0
    y_velocity = 0

    speed = 0

    sprite_path = None

    def __init__(self, game):
        if self.sprite_path is not None:
            self.sprite = pygame.image.load(self.sprite_path)

        self.game = game
        self.alive = True

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def destroy(self):
        self.game.entities.remove(self)
        self.alive = False


class Punch(Entity):
    sprite_path = os.path.join(IMAGE_FOLDER, 'punch', '1f91c.png')

    time_spawned = 0
    time_alive = 0.3

    def __init__(self, game, player):
        super().__init__(game)

        self.time_spawned = time.time()
        self.player = player

        self.update()

    @classmethod
    def spawn(cls, player):
        sprite = cls(game=player.game, player=player)
        sprite.game.entities.append(sprite)

        return sprite

    @property
    def expiry_time(self):
        return self.time_spawned + self.time_alive

    def update(self):
        if not self.alive:
            return

        self.x = self.player.x + self.width
        self.y = self.player.y

        now = time.time()
        if now >= self.expiry_time:
            self.destroy()


class Player(Entity):
    speed = 10
    sprite_path = os.path.join(IMAGE_FOLDER, 'player.png')

    def __init__(self, game):
        super().__init__(game)

        self._punch = None

    def punch(self, direction):
        if self._punch is None or not self._punch.alive:
            punch = Punch.spawn(player=self)
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

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
