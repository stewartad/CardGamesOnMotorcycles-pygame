import pygame
from pygame import sprite

import constants as c
from ui_elements import *


class HandView:
    def __init__(self, x, y, player):
        self.player = player
        self.sprites = []
        self.sprites_group = sprite.Group()
        self.rect = pygame.Rect(x, y, c.HAND_W, c.HAND_H)

    def draw(self, surface_obj):
        self.sprites_group.draw(surface_obj)

    def update(self):
        self.sprites_group.empty()
        self.sprites.clear()
        i = 0
        for card in self.player.hand:
            self.sprites.append(SmallCardSprite(card, (c.S_CARD_WIDTH * i) + (i + 1) * c.CARD_GAP, self.rect.y))
            i = i + 1
        self.sprites_group.add(self.sprites)
        self.sprites_group.update()


class FieldView:
    def __init__(self, x, y, player):
        self.player = player
        self.sprites = []
        self.sprites_group = sprite.Group()
        self.rect = pygame.Rect(x, y, c.HAND_W, c.HAND_H)
        self.field = {
            'top-left': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 0, c.FIELD_TOP + c.FIELD_ZONE_H * 0),
            'top-center': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 1, c.FIELD_TOP + c.FIELD_ZONE_H * 0),
            'top-right': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 2, c.FIELD_TOP + c.FIELD_ZONE_H * 0),
            'bot-left': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 0, c.FIELD_TOP + c.FIELD_ZONE_H * 1),
            'bot-center': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 1, c.FIELD_TOP + c.FIELD_ZONE_H * 1),
            'bot-right': FieldSlot(c.FIELD_LEFT + c.FIELD_ZONE_W * 2, c.FIELD_TOP + c.FIELD_ZONE_H * 1)
        }
        self.sprites_group.add(self.field.values())

    def draw(self, surface_obj):
        for field_zone in self.field.values():
            pygame.draw.rect(surface_obj, c.BLACK, field_zone.rect, 1)
        self.sprites_group.draw(surface_obj)

    def get_location(self, x, y):
        for location in self.field.keys():
            if self.field[location].rect.collidepoint(x, y):
                return location
        return None

    def update(self):
        self.sprites_group.empty()
        # self.sprites.clear()
        # i = 0
        # for card in self.player.field.card_field.values():
        #     self.sprites.append(CardSprite(card, (c.CARD_WIDTH * i) + (i + 1) * c.CARD_GAP, self.rect.y))
        #     i = i + 1
        # self.sprites_group.add(self.sprites)
        for location in self.player.field.card_field.keys():
            self.field[location].place_card(self.player.field.card_field[location])
        self.sprites_group.add(self.field.values())
        self.sprites_group.update()