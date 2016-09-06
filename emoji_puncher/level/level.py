# coding=utf-8
import pygame

from ..entity import Gate
from ..spritesheet import SpriteSheet

__all__ = ['TestLevel']

class Level(object):
    background_path = ('images', 'background.png')

    def __init__(self, player):
        self.entity_list = pygame.sprite.Group()
        self.player = player
        self.player.level = self

        self.populate_stage()

        self.entity_list.add()

        self.background = SpriteSheet(*self.background_path).get_image(0, 0, 2100, 600)
        self.level_width = self.background.get_width()
        self.level_height = self.background.get_height()

        self.camera = Camera(complex_camera, self.level_width, self.level_height)

    def populate_stage(self):
        raise NotImplementedError()

    def update(self, time_passed):
        self.camera.update(self.player)
        self.entity_list.update(time_passed)
        self.player.update(time_passed)

    def draw(self, screen):
        screen.blit(self.background, self.camera.apply_to_background(self.background))

        for entity in self.entity_list:
            screen.blit(entity.image, self.camera.apply(entity))

        screen.blit(self.player.image, self.camera.apply(self.player))

        pygame.display.flip()


class TestLevel(Level):
    background_path = ('images', 'background_test_level.png')

    def populate_stage(self):
        gate = Gate(level=self)
        gate.rect.x = 300
        gate.rect.y = 300

        self.entity_list.add(gate)

        gate = Gate(level=self)
        gate.rect.x = 250
        gate.rect.y = 400

        self.entity_list.add(gate)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.rect.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def apply_to_background(self, background):
        return background.get_rect().move(self.state.topleft)

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
