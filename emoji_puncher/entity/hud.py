# coding=utf-8
import os

from .entity import Entity
from ..constant import IMAGE_FOLDER


class Hud(Entity):
    sprite_path = os.path.join(IMAGE_FOLDER, 'hud.png')

    def __init__(self, game):
        super(Hud, self).__init__(game)

        self.alive = True

    def render(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        screen.blit(self.game.player.sprite, (730, 329))
