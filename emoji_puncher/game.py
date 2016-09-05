# coding=utf-8
import sys

import pygame

from .constant import MAX_ENEMIES, ENEMY_SPAWN_COOLDOWN, HUD_HEIGHT
from .entity import Player, Enemy, Hud


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

        self.player = Player.spawn(game=self)
        self.spawner = EnemySpawner(game=self)
        self.hud_controller = HudController(game=self)
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

            if not self.pause:
                self.spawner.update()

            self.hud_controller.update()
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


class HudController(object):
    def __init__(self, game):
        self.game = game
        self.hud = Hud.spawn(game=game)

    def update(self):
        pass