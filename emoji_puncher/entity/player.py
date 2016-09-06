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
        if not self.falling:
            self.y_velocity = self.jump_velocity
            self.falling = True

    def process_keydown(self, key):
        if key == pygame.K_LEFT:
            self.moving = True
            self.direction = Direction.LEFT

        elif key == pygame.K_RIGHT:
            self.moving = True
            self.direction = Direction.RIGHT

        elif key == pygame.K_UP:
            self.jump()

    def check_for_movement_keys(self):
        pressed_keys = pygame.key.get_pressed()

        moving_left = pressed_keys[pygame.K_LEFT]
        moving_right = pressed_keys[pygame.K_RIGHT]

        if self.direction == Direction.LEFT and moving_left:
            self.x_velocity -= self.acceleration
        elif self.direction == Direction.RIGHT and moving_right:
            self.x_velocity += self.acceleration

        if self.direction == Direction.LEFT and moving_right:
            self.x_velocity = self.deacceleration
        elif self.direction == Direction.RIGHT and moving_left:
            self.x_velocity = self.deacceleration

        if not (moving_left or moving_right):
            self.apply_friction()
