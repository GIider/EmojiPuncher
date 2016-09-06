# coding=utf-8
from .entity import Entity

__all__ = ['Gate', 'GrassyPlatformLeft', 'GrassyPlatformMid', 'GrassyPlatformRight']


class BasePlatform(Entity):
    def calculate_gravity(self, time_passed):
        return


class Gate(Entity):
    walking_sprite_sheet = ('images', 'tile.png')
    walking_cycle = [(0, 0, 64, 64)]


class GrassyPlatformLeft(BasePlatform):
    walking_sprite_sheet = ('images', 'grassHalfLeft.png')
    walking_cycle = [(0, 0, 64, 64)]


class GrassyPlatformMid(BasePlatform):
    walking_sprite_sheet = ('images', 'grassHalfMid.png')
    walking_cycle = [(0, 0, 64, 64)]


class GrassyPlatformRight(BasePlatform):
    walking_sprite_sheet = ('images', 'grassHalfRight.png')
    walking_cycle = [(0, 0, 64, 64)]
