# coding=utf-8
import sys

import pygame

from .player import Player
from .constant import Direction, DIRECTION_KEYS


class Game(object):
    WIDTH = 800
    HEIGHT = 400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('EmojiPuncher')

        self.player = Player(game=self)
        self.entities = [self.player]

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.quit()
        elif key in DIRECTION_KEYS:
            self.player.move(direction=Direction.from_key(key=key))
        elif key == pygame.K_SPACE:
            self.player.punch()

    def handle_keyup(self, key):
        if key in DIRECTION_KEYS:
            self.player.stop(direction=Direction.from_key(key=key))

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(key=event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(key=event.key)
                elif event.type == pygame.QUIT:
                    self.quit()

            clock.tick(60)
            self.screen.fill((0, 0, 0))
            for entity in self.entities:
                entity.render(screen=self.screen)

            pygame.display.flip()
            for entity in self.entities:
                entity.update()


game = Game()
game.run()
