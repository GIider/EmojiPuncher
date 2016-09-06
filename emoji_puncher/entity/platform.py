# coding=utf-8
from .entity import Entity


class Gate(Entity):
    walking_sprite_sheet = ('images', 'tile.png')
    walking_cycle = [(0, 0, 64, 64)]

    def calculate_gravity(self, time_passed):
        return
