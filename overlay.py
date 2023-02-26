import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        overlay_path = 'resources/graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png') for tool in player.tools}
        self.goods_surf = {good: pygame.image.load(f'{overlay_path}{good}.png') for good in player.goods}

        self.font = pygame.font.Font('resources/font/LycheeSoda.ttf', 30)

    def display(self):
        tools_surf = self.tools_surf[self.player.selected_tool]
        tools_rect = tools_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])

        goods_surf = self.goods_surf[self.player.selected_good]
        goods_rect = goods_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])

        msg = self.font.render(str(self.player.pack[self.player.selected_good]), True, 'black')
        msg_rect = msg.get_rect(midbottom=OVERLAY_POSITIONS['number'])

        self.display_surface.blit(tools_surf, tools_rect)
        self.display_surface.blit(goods_surf, goods_rect)
        self.display_surface.blit(msg, msg_rect)
