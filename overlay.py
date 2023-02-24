import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player

        overlay_path = 'resources/graphics/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png') for tool in player.tools}

    def display(self):
        tools_surf = self.tools_surf[self.player.selected_tool]
        tools_rect = tools_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tools_surf, tools_rect)
