# coding=utf-8
import pygame

__all__ = ['Entity']


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