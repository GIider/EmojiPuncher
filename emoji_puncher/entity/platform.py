# coding=utf-8
from .entity import Entity


class Gate(Entity):
    walking_sprite_sheet = ('images', 'tile.png')
    walking_cycle = [(0, 0, 64, 64)]

    def check_for_movement_keys(self):
        pass
