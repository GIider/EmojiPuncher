# coding=utf-8
import pygame

from ..entity import Gate
from ..spritesheet import SpriteSheet


class Level(object):
    background_path = ('images', 'background.png')

    def __init__(self, player):
        self.entity_list = pygame.sprite.Group()
        self.player = player

        gate = Gate()
        gate.rect.x = 300
        gate.rect.y = 300

        self.entity_list.add(self.player)
        self.entity_list.add(gate)

        self.background = SpriteSheet(*self.background_path).get_image(0, 0, 2100, 600)

    def update(self, time_passed):
        self.entity_list.update(time_passed)
        self.player.update(time_passed)

    def draw(self, screen):
        screen.blit(self.background, (0, -200))
        self.entity_list.draw(screen)

        pygame.display.flip()


class TestLevel(Level):
    pass
