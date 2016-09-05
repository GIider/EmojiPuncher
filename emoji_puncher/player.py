# coding=utf-8
import random
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
        self.sprite = None
        self.game = game
        self.alive = True

        self.load_sprite(path=self.sprite_path)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def load_sprite(self, path):
        if path is not None:
            self.sprite = pygame.image.load(path).convert_alpha()

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))

    def destroy(self):
        self.game.entities.remove(self)
        self.alive = False

    def update(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def colliding(self, other_entity):
        return self.rect.colliderect(other_entity.rect)


class Punch(Entity):
    time_spawned = 0
    time_alive = 0.3

    punch_images = {Direction.LEFT: os.path.join(IMAGE_FOLDER, 'punch', '1f91b.png'),
                    Direction.RIGHT: os.path.join(IMAGE_FOLDER, 'punch', '1f91c.png')}

    def __init__(self, game, player, direction):
        super().__init__(game)

        self.time_spawned = time.time()
        self.player = player
        self.direction = direction

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
            if isinstance(entity, Enemy) and self.colliding(entity):
                entity.destroy()

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


class Enemy(Entity):
    speed = 5
    sprite_path = os.path.join(IMAGE_FOLDER, 'enemy.png')

    def __init__(self, game, spawner):
        super().__init__(game)

        self.spawner = spawner

        self.x = random.choice([0, game.WIDTH])
        self.y = random.randrange(0, game.HEIGHT - self.height)

        if self.x == 0:
            self.x_velocity = self.speed
        else:
            self.x_velocity -= self.speed

    def update(self):
        super(Enemy, self).update()

        if self.x >= self.game.WIDTH or self.x <= 0:
            self.destroy()

    def destroy(self):
        super(Enemy, self).destroy()

        self.spawner.killed(self)