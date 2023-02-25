import random
import pygame
from pygame.sprite import AbstractGroup
from settings import *


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, z, *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.7, -self.rect.height*0.75)


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
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.8, -self.rect.height*0.98)


class Tree(Generic):
    def __init__(self, pos, surf, z, name, *groups: AbstractGroup):
        super().__init__(pos, surf, z, *groups)
        self.apples_surf = pygame.image.load(r'resources/graphics/fruit/apple.png')
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()

        self.health = 4
        self.is_alive = Tree
        self.stump_surf = pygame.image.load(f'resources/graphics/objects/stump_{"small" if name == "Small" else "medium"}.png')

        self.create_fruit()

    def damage(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.7, -self.rect.height * 0.75)
            self.is_alive = False
        elif self.health > 0:
            self.health -= 1
            if len(self.apple_sprites) > 0:
                random_apple = random.choice(self.apple_sprites.sprites())
                random_apple.kill()

    def create_fruit(self):
        random_array = random.sample(range(0, 6), random.randint(1, 2))
        for index in random_array:
            pos = self.apple_pos[index]
            x = self.rect.left + pos[0]
            y = self.rect.top + pos[1]
            Generic((x, y), self.apples_surf, LAYERS['fruit'], *(self.apple_sprites, self.groups()[0]))

