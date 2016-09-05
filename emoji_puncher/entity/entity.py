# coding=utf-8
import os

import pygame

from ..constant import IMAGE_FOLDER

__all__ = ['Entity', 'TimedEntity']

LOADED_IMAGES = {}


class Entity(object):
    width = 64
    height = 64

    x_velocity = 0
    y_velocity = 0

    maximum_x_velocity = 2.5
    maximum_y_velocity = 2.5

    minimum_x_velocity = -1 * maximum_x_velocity
    minimum_y_velocity = -1 * maximum_y_velocity

    speed = 0
    friction = 0.08

    sprite_path = os.path.join(IMAGE_FOLDER, 'placeholder.png')

    def __init__(self, game):
        self.game = game
        self.alive = True

        self.x = 0
        self.y = 0

        self.sprite = self.load_sprite(path=self.sprite_path)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @classmethod
    def spawn(cls, game, **kwargs):
        sprite = cls(game=game, **kwargs)
        sprite.game.entities.append(sprite)

        return sprite

    def load_sprite(self, path):
        try:
            sprite = LOADED_IMAGES[path].copy()
        except KeyError:
            sprite = pygame.image.load(path).convert_alpha()
            LOADED_IMAGES[path] = sprite

        return sprite

    def load_position(self):
        """Called before rendering to change the location of the object"""
        pass

    def render(self, screen):
        self.load_position()
        screen.blit(self.sprite, (self.x, self.y))

    def destroy(self):
        self.alive = False

    def update(self, time_passed):
        self.x += self.x_velocity * time_passed
        self.y += self.y_velocity * time_passed

    def colliding(self, other_entity):
        return self.rect.colliderect(other_entity.rect)


class TimedEntity(Entity):
    """Entity that dies automatically"""
    time_alive = 0  # In milliseconds

    def __init__(self, game):
        super().__init__(game)

        self.time_spawned = pygame.time.get_ticks()

    @property
    def expiry_time(self):
        return self.time_spawned + self.time_alive

    def update(self, time_passed):
        now = pygame.time.get_ticks()
        if now >= self.expiry_time:
            self.destroy()
