# coding=utf-8
import sys

import pygame

from .entity import Player
from .level import TestLevel


def quit_application():
    pygame.quit()
    sys.exit()


class Game(object):
    width = 800
    height = 400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('EmojiPuncher')

        self.player = Player(level=None)
        self.clock = pygame.time.Clock()

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            quit_application()

        self.player.process_keydown(key)

    def run(self):
        TestLevel.load_stage(player=self.player)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(key=event.key)
                elif event.type == pygame.QUIT:
                    quit_application()

            time_passed = self.clock.tick(60)
            self.screen.fill((255, 255, 255))

            self.player.level.draw(self.screen)
            self.player.level.update(time_passed)
