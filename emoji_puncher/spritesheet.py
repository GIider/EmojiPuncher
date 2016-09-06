import os

import pygame


class SpriteSheet(object):
    sprite_sheet = None

    def __init__(self, *path_components):
        file_name = os.path.join(os.path.dirname(__file__), *path_components)
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height], flags=pygame.SRCALPHA)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        return image
