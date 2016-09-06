# coding=utf-8
import pygame

from ..constant import Direction
from ..spritesheet import SpriteSheet


class Entity(pygame.sprite.Sprite):
    jump_velocity = -4
    acceleration = 0.08963  # 0.046875
    deacceleration = 0.5
    gravity = 0.21875 / 16

    friction = 0.08
    maximum_run_speed = 5
    maximum_fall_speed = 16

    cycle_frame_rate = 120

    walking_sprite_sheet = ('images', 'player.png')
    walking_cycle = [(0, 0, 64, 64),
                     (64, 0, 64, 64)]

    def __init__(self, level):
        """ Constructor function """
        pygame.sprite.Sprite.__init__(self)

        self.x_velocity = 0
        self.y_velocity = 0

        self.falling = True
        self.moving = False

        # Walking animations
        self.walking_frames_l = []
        self.walking_frames_r = []

        self.direction = Direction.RIGHT
        self.load_walking_frames()

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()

        self.level = level

    def load_walking_frames(self):
        sprite_sheet = SpriteSheet(*self.walking_sprite_sheet)

        for x, y, width, height in self.walking_cycle:
            image = sprite_sheet.get_image(x, y, width, height)
            self.walking_frames_r.append(image)

            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

    def animate_sprite(self):
        """Cycle the walking frames"""
        ticks = pygame.time.get_ticks()

        if self.direction == "R":
            frame = (ticks // self.cycle_frame_rate) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (ticks // self.cycle_frame_rate) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

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

    def calculate_gravity(self, time_passed):
        if self.falling:
            self.y_velocity += self.gravity * time_passed

            if self.y_velocity >= self.maximum_fall_speed:
                self.y_velocity = self.maximum_fall_speed

    def apply_friction(self):
        self.x_velocity = self.x_velocity - min(abs(self.x_velocity), self.friction) * self.x_velocity
        self.y_velocity = self.y_velocity - min(abs(self.y_velocity), self.friction) * self.y_velocity

    def update(self, time_passed):
        self.animate_sprite()
        self.calculate_gravity(time_passed)

        if self.moving:
            self.check_for_movement_keys()

        if self.x_velocity == 0:
            self.moving = False
            self.direction = None

        self.move_sprite()

    def move_sprite(self):
        self.x_velocity = max(min(self.x_velocity, self.maximum_run_speed), -self.maximum_run_speed)

        self.rect.x = min(max(self.rect.x + self.x_velocity, 0), self.level.level_width)
        self.rect.y = min(max(self.rect.y + self.y_velocity, 0), self.level.level_height)

        if self.rect.y > (self.level.level_height - self.rect.height):
            self.falling = False
            self.y_velocity = 0
            self.rect.y = self.level.level_height - self.rect.height

        if self.rect.x > (self.level.level_width - self.rect.width):
            self.moving = False
            self.x_velocity = 0
            self.rect.x = self.level.level_width - self.rect.width
