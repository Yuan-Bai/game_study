from settings import *
import pygame


class Pack:
    def __init__(self, player, toggle_menu):
        self.width = 400
        self.height = 0
        self.padding = 8
        self.space = 10
        self.main_rect = pygame.Rect
        self.keys = player.pack.keys()
        self.player = player
        self.index = 0
        self.timers = player.timers
        self.toggle_menu = toggle_menu
        self.font = pygame.font.Font('resources/font/LycheeSoda.ttf', 30)
        self.text_surfs = []
        self.display_surface = pygame.display.get_surface()
        self.setup()

    def setup(self):
        for item in self.keys:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.height += text_surf.get_height() + 2*self.padding
        self.height += (len(self.text_surfs)-1) * self.space
        pack_top = SCREEN_HEIGHT/2 - self.height/2
        pack_left = SCREEN_WIDTH/2 - self.width/2
        self.main_rect = pygame.Rect(pack_left, pack_top, self.width, self.height)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['toggle_menu'].active:
            if keys[pygame.K_TAB] or keys[pygame.K_ESCAPE]:
                self.toggle_menu()
                self.player.selected_good = self.player.goods[self.index]
                self.timers['toggle_menu'].activate()
            if not self.timers['tool_switch'].active:
                if keys[pygame.K_w]:
                    self.index -= 1
                    if self.index < 0:
                        self.index = 3
                    self.timers['tool_switch'].activate()
                if keys[pygame.K_s]:
                    self.index += 1
                    if self.index > 3:
                        self.index = 0
                    self.timers['tool_switch'].activate()

    def update(self):
        self.input()
        self.timer_update()

        for text_index, surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index*(surf.get_height()+self.padding*2+self.space)

            # background
            bg_rect = pygame.Rect(self.main_rect.left, top, self.width, surf.get_height() + (self.padding * 2))
            pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

            # text
            text_rect = surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
            self.display_surface.blit(surf, text_rect)

            # amount todo
            amount_surf = self.font.render(str(list(self.player.pack.values())[text_index]), False, 'Black')
            amount_rect = amount_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery))
            self.display_surface.blit(amount_surf, amount_rect)

            if self.index == text_index:
                pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
