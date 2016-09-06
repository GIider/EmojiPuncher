# coding=utf-8
import os

import pygame

from ..constant import TILE_SIZE
from ..entity import Gate

__all__ = ['TestLevel']


class Level(object):
    logic_path = ('level.bmp',)

    def __init__(self, player):
        self.entity_list = pygame.sprite.Group()
        self.player = player
        self.player.level = self

        self.populate_stage()

        self.entity_list.add()

        logic_image = self.load_logic_image()

        self.width = logic_image.get_width() * TILE_SIZE[0]
        self.height = logic_image.get_height() * TILE_SIZE[1]

        self.camera = Camera(complex_camera, self.width, self.height)

    def load_logic_image(self):
        image_path = os.path.join(os.path.dirname(__file__), *self.logic_path)
        image = pygame.image.load(image_path).convert()

        return image

    def populate_stage(self):
        image = self.load_logic_image()

        for x in range(0, image.get_width()):
            for y in range(0, image.get_height()):
                color = image.get_at((x, y))

                # Gate
                if color == (0, 0, 0, 255):
                    gate = Gate(level=self)
                    gate.rect.x = x * gate.rect.width
                    gate.rect.y = y * gate.rect.height

                    self.entity_list.add(gate)

                # Spawn Point
                elif color == (255, 0, 220):
                    self.player.rect.x = x * self.player.rect.width
                    self.player.rect.y = y * self.player.rect.height

    def update(self, time_passed):
        self.camera.update(self.player)
        self.entity_list.update(time_passed)
        self.player.update(time_passed)

    def draw(self, screen):
        for entity in self.entity_list:
            screen.blit(entity.image, self.camera.apply(entity))

        screen.blit(self.player.image, self.camera.apply(self.player))

        pygame.display.flip()


class TestLevel(Level):
    logic_path = ('testlevel.bmp',)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.rect.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + 400, -t + 200, w, h  # center player

    l = min(0, l)  # stop scrolling at the left edge
    l = max(-(camera.width - 800), l)  # stop scrolling at the right edge
    t = max(-(camera.height - 400), t)  # stop scrolling at the bottom
    t = min(0, t)  # stop scrolling at the top

    return pygame.rect.Rect(l, t, w, h)
