# coding=utf-8
import sys

import pygame

from .constant import HUD_HEIGHT
from .entity import Player


def quit_application():
    pygame.quit()
    sys.exit()


class Game(object):
    width = 800
    height = 400

    playable_width = width
    playable_height = height - HUD_HEIGHT

    def __init__(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('EmojiPuncher')

        self.entities = []

        self.player = Player()
        self.clock = pygame.time.Clock()
        self.pause = False

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            quit_application()

        elif key == pygame.K_p:
            self.pause = not self.pause

        if not self.pause:
            self.player.process_keydown(key)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(key=event.key)
                elif event.type == pygame.QUIT:
                    quit_application()

            time_passed = self.clock.tick(60)
            self.screen.fill((255, 255, 255))
            for entity in self.entities:
                entity.render(screen=self.screen)

            pygame.display.flip()
            for entity in self.entities[:]:
                if entity.alive and not self.pause:
                    entity.update(time_passed=time_passed)
                elif not entity.alive:
                    self.entities.remove(entity)
