# coding=utf-8
import os

from .entity import Entity
from ..constant import IMAGE_FOLDER


class Hud(Entity):
    sprite_path = os.path.join(IMAGE_FOLDER, 'hud.png')
