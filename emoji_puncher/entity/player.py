# coding=utf-8
import pygame

from .entity import Entity
from ..constant import Direction


class Player(Entity):
    cycle_frame_rate = 120

    walking_sprite_sheet = ('images', 'player.png')
    walking_cycle = [(0, 0, 64, 64),
                     (64, 0, 64, 64)]

    def jump(self):
        if self.standing_on_ground():
            self.y_velocity = self.jump_velocity

    def enter(self):
        entities = pygame.sprite.spritecollide(self, self.level.entity_list, False)

        for entity in entities:
            entity.interact()

    def process_keydown(self, key):
        if key == pygame.K_LEFT:
            self.moving = True
            self.direction = Direction.LEFT

        elif key == pygame.K_RIGHT:
            self.moving = True
            self.direction = Direction.RIGHT

        elif key == pygame.K_UP:
            self.jump()

        elif key == pygame.K_DOWN:
            self.enter()

    def check_for_movement_keys(self):
        pressed_keys = pygame.key.get_pressed()

        moving_left = pressed_keys[pygame.K_LEFT]
        moving_right = pressed_keys[pygame.K_RIGHT]

        if not moving_left and not moving_right:
            self.x_velocity = 0

        if self.direction == Direction.LEFT and moving_left:
            self.x_velocity = -self.acceleration
        elif self.direction == Direction.RIGHT and moving_right:
            self.x_velocity = self.acceleration

        if self.direction == Direction.LEFT and moving_right:
            self.x_velocity = -self.deacceleration
        elif self.direction == Direction.RIGHT and moving_left:
            self.x_velocity = self.deacceleration

    def update(self, time_passed):
        self.check_for_movement_keys()

        super(Player, self).update(time_passed)
