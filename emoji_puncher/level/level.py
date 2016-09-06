# coding=utf-8
import os

import pygame

from ..constant import TILE_SIZE, GAME_SIZE
from ..entity import WarpDoor, GrassyPlatformMid, GrassyPlatformRight, GrassyPlatformLeft

__all__ = ['TestLevel']


class Level(object):
    logic_path = ('level.bmp',)

    def __init__(self, player):
        self.entity_list = pygame.sprite.Group()
        self.player = player
        self.spawn_point = None

        logic_image = self.load_logic_image()

        self.width = logic_image.get_width() * TILE_SIZE[0]
        self.height = logic_image.get_height() * TILE_SIZE[1]

        self.camera = Camera(complex_camera, self.width, self.height)

    @classmethod
    def load_stage(cls, player):
        if player.level is not None:
            player.level.leave_stage()

        level = cls(player)
        level.populate_stage()

        level.player.level = level
        level.player.rect.x = level.spawn_point[0] * level.player.rect.width
        level.player.rect.y = level.spawn_point[1] * level.player.rect.height

        return level

    def leave_stage(self):
        self.entity_list = pygame.sprite.Group()
        self.player.level = None

    def load_logic_image(self):
        image_path = os.path.join(os.path.dirname(__file__), *self.logic_path)
        image = pygame.image.load(image_path).convert()

        return image

    def populate_stage(self):
        image = self.load_logic_image()

        for x in range(0, image.get_width()):
            for y in range(0, image.get_height()):
                color = image.get_at((x, y))

                # Platform
                if color == (0, 0, 0, 255):
                    try:
                        platform_left = image.get_at((x + 1, y)) == (0, 0, 0, 255)
                    except IndexError:
                        platform_left = False

                    try:
                        platform_right = image.get_at((x - 1, y)) == (0, 0, 0, 255)
                    except IndexError:
                        platform_right = False

                    if platform_left and platform_right:
                        platform = GrassyPlatformMid(level=self)
                    elif platform_left and not platform_right:
                        platform = GrassyPlatformRight(level=self)
                    elif not platform_left and platform_right:
                        platform = GrassyPlatformLeft(level=self)
                    else:
                        platform = GrassyPlatformMid(level=self)

                    platform.rect.x = x * platform.rect.width
                    platform.rect.y = y * platform.rect.height

                    self.entity_list.add(platform)

                # Spawn Point
                elif color == (255, 0, 220):
                    self.spawn_point = [x, y]

                # Warp door
                elif color == (255, 0, 0):
                    warpdoor = WarpDoor(level=self, level_to_warp_to=OtherLevel)
                    warpdoor.rect.x = x * warpdoor.rect.width
                    warpdoor.rect.y = y * warpdoor.rect.height

                    self.entity_list.add(warpdoor)

        if self.spawn_point is None:
            raise ValueError()

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


class OtherLevel(Level):
    logic_path = ('otherlevel.bmp',)


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
    l, t, _, _ = -l + GAME_SIZE.width / 2, -t + GAME_SIZE.height / 2, w, h  # center player

    l = min(0, l)  # stop scrolling at the left edge
    l = max(-(camera.width - GAME_SIZE.width), l)  # stop scrolling at the right edge
    t = max(-(camera.height - GAME_SIZE.height), t)  # stop scrolling at the bottom
    t = min(0, t)  # stop scrolling at the top

    return pygame.rect.Rect(l, t, w, h)
