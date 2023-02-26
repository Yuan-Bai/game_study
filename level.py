import pygame
from player import Player
from settings import *
from overlay import Overlay
from sprites import Generic, Water, Tree, WildFlower
from pytmx.util_pygame import load_pygame
from support import import_folder


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.player = None
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        # 世界
        Generic((0, 0),
                pygame.image.load(r'resources/graphics/world/ground.png'),
                LAYERS['ground'],
                self.all_sprites)
        tmx_data = load_pygame(r'resources/data/map.tmx')
        # 玩家
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.tree_sprites, self.collision_sprites)
        # 房子
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x*TILE_SIZE, y*TILE_SIZE), surf, LAYERS['house bottom'], self.all_sprites)
        for layer in ['HouseWalls', 'HouseFurnitureTop', 'Fence']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, LAYERS['main'], *(self.all_sprites, self.collision_sprites))
        # 树
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree((obj.x, obj.y), obj.image, LAYERS['main'], obj.name, self.player.pack, *(self.all_sprites, self.collision_sprites, self.tree_sprites))
        # 花
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, LAYERS['main'], *(self.all_sprites, self.collision_sprites))
        # 水
        water_frames = import_folder(r'resources/graphics/water')
        for x, y, _ in tmx_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, LAYERS['water'], self.all_sprites)
        # collision tiles
        for x, y, _ in tmx_data.get_layer_by_name('Collision').tiles():
            Generic((x*TILE_SIZE, y*TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), LAYERS['main'], self.collision_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.customize_draw(self.player)
        self.all_sprites.update(dt)
        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super(CameraGroup, self).__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH/2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT/2
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # if sprite.z == LAYERS['main']:
                    #     hitbox_rect = sprite.hitbox.copy()
                    #     hitbox_rect.center -= self.offset
                    #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
