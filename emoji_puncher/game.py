# coding=utf-8
import sys

import pygame

from .constant import MAX_ENEMIES, ENEMY_SPAWN_COOLDOWN
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
        self.pause = False

        self.entities = [self.player]

    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.quit()

        elif key == pygame.K_p:
            self.pause = not self.pause

        if not self.pause:
            self.player.process_keydown(key)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(key=event.key)
                elif event.type == pygame.QUIT:
                    self.quit()

            time_passed = self.clock.tick(60)
            self.screen.fill((255, 255, 255))
            for entity in self.entities:
                entity.render(screen=self.screen)

            pygame.display.flip()

            if not self.pause:
                self.spawner.update()

            for entity in self.entities[:]:
                if entity.alive and not self.pause:
                    entity.update(time_passed=time_passed)
                elif not entity.alive:
                    self.entities.remove(entity)


class EnemySpawner(object):
    def __init__(self, game):
        self.enemies_spawned = 0
        self.enemies = []

        self.game = game
        self.last_spawn = pygame.time.get_ticks()

    @property
    def can_spawn(self):
        now = pygame.time.get_ticks()

        return now >= (self.last_spawn + ENEMY_SPAWN_COOLDOWN) and \
               len(self.enemies) <= MAX_ENEMIES

    def update(self):
        if self.can_spawn:
            self.spawn()

    def spawn(self):
        enemy = Enemy.spawn(game=self.game, spawner=self)
        self.enemies.append(enemy)

        self.last_spawn = pygame.time.get_ticks()

    def killed(self, enemy):
        self.enemies.remove(enemy)
