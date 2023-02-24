import pygame
from pygame.sprite import AbstractGroup
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, z, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.8, -self.rect.height*0.75)


class Water(Generic):
    def __init__(self, pos, frames, z, *groups: AbstractGroup):
        super().__init__(pos, frames[0], z, *groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.pos = pos

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt) -> None:
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos, surf, z, *groups: AbstractGroup):
        super().__init__(pos, surf, z, *groups)
        self.hitbox = self.rect.copy().inflate(--self.rect.width*0.8, -self.rect.height*0.9)


class Tree(Generic):
    def __init__(self, pos, surf, z, *groups: AbstractGroup):
        super().__init__(pos, surf, z, *groups[:2])

