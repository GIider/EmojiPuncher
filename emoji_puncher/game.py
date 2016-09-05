# coding=utf-8
import random
import sys

import pygame

from .constant import Direction, DIRECTION_KEYS, PUNCHING_KEYS, MAX_ENEMIES
from .entity import Player, Enemy


class Game(object):
    WIDTH = 800
    HEIGHT = 400

    def __init__(self):
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('EmojiPuncher')

        self.player = Player(game=self)
        self.spawner = EnemySpawner(game=self)
        self.clock = pygame.time.Clock()

        self.entities = [self.player]

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.quit()
        elif key in DIRECTION_KEYS:
            self.player.move(direction=Direction.from_key(key=key))
        elif key in PUNCHING_KEYS:
            self.player.punch(direction=Direction.from_key(key=key))

    def handle_keyup(self, key):
        if key in DIRECTION_KEYS:
            self.player.stop(direction=Direction.from_key(key=key))

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(key=event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(key=event.key)
                elif event.type == pygame.QUIT:
                    self.quit()

            time_passed = self.clock.tick(60)
            self.screen.fill((255, 255, 255))
            for entity in self.entities:
                entity.render(screen=self.screen)

            pygame.display.flip()

            self.spawner.update()
            for entity in self.entities:
                entity.update(time_passed=time_passed)


class EnemySpawner(object):
    def __init__(self, game):
        self.enemies_spawned = 0
        self.enemies = []

        self.game = game

    def update(self):
        if len(self.enemies) <= MAX_ENEMIES and random.randint(0, 100) <= 10:
            self.spawn()

    def spawn(self):
        enemy = Enemy(game=self.game, spawner=self)

        self.enemies.append(enemy)
        self.game.entities.append(enemy)

    def killed(self, enemy):
        self.enemies.remove(enemy)
