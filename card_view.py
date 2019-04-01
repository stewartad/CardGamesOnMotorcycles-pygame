import pygame
from pygame import sprite

import constants
from ui_elements import SmallCardSprite, CardSprite


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

    def draw(self, surface_obj):
        self.sprites_group.draw(surface_obj)

    def update(self):
        self.sprites_group.empty()
        self.sprites.clear()
        i = 0
        for card in self.player.field:
            self.sprites.append(CardSprite(card, (c.CARD_WIDTH * i) + (i + 1) * c.CARD_GAP, self.rect.y))
            i = i + 1
        self.sprites_group.add(self.sprites)
        self.sprites_group.update()