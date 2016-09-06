# coding=utf-8
from .entity import Entity

__all__ = ['WarpDoor']


class WarpDoor(Entity):
    solid = False

    walking_sprite_sheet = ('images', 'door.png')
    walking_cycle = [(0, 0, 64, 64)]

    def __init__(self, level, level_to_warp_to):
        super(WarpDoor, self).__init__(level)

        self.level_to_warp_to = level_to_warp_to

    def interact(self):
        self.level_to_warp_to.load_stage(self.level.player)
