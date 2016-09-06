# coding=utf-8
import pygame

from ..spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    cycle_frame_rate = 120

    walking_sprite_sheet = ('images', 'player.png')
    walking_cycle = [(0, 0, 64, 64),
                     (64, 0, 64, 64)]

    def __init__(self):
        """ Constructor function """
        pygame.sprite.Sprite.__init__(self)

        # Walking animations
        self.walking_frames_l = []
        self.walking_frames_r = []

        self.direction = "R"
        self.load_walking_frames()

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]
        self.rect = self.image.get_rect()

        self.level = None

    def load_walking_frames(self):
        sprite_sheet = SpriteSheet(*self.walking_sprite_sheet)

        for x, y, width, height in self.walking_cycle:
            image = sprite_sheet.get_image(x, y, width, height)
            self.walking_frames_r.append(image)

            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)

    def animate_sprite(self):
        """Cycle the walking frames"""
        pos = self.rect.x + self.level.world_shift

        if self.direction == "R":
            frame = (pos // self.cycle_frame_rate) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // self.cycle_frame_rate) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
