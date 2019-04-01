import math

import pygame

import constants
from game_ui import State
from ui_elements import SmallCardSprite


class CardLayer(State):
    def __init__(self, game_state):
        super(CardLayer, self).__init__(game_state)
        self.image = pygame.Surface((c.OVER_W, c.OVER_H))
        self.rect = pygame.Rect(c.OVER_CORNER, (c.OVER_W, c.OVER_H))
        self.card_list = []
        self.sprites = []
        self.next = 'board'

    def create_card_sprites(self):
        self.active_sprites.empty()
        i = 0
        for card in self.card_list:
            col = i
            row = math.floor(i / 3)
            if col % 3 == 0:
                col = 0
            elif col % 3 == 1:
                col = 1
            elif col % 3 == 2:
                col = 2
            self.sprites.append((SmallCardSprite(card, (col * (c.S_CARD_WIDTH + c.CARD_GAP)) + c.CARD_GAP,
                                                 self.rect.y + row * c.CARD_HEIGHT)))
            i = i + 1
        self.active_sprites.add(self.sprites)

    def on_click(self, x, y):
        self.done = True

    def draw(self, surface_obj):
        self.preview.draw(surface_obj)
        self.active_sprites.draw(self.image)
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.DARKGRAY)
        self.sprites.clear()
        self.create_card_sprites()
        self.active_sprites.update()
        self.preview.update()


class DeckLayer(CardLayer):
    def __init__(self, game_state):
        super(DeckLayer, self).__init__(game_state)
        self.card_list = self.game_state.player.deck.deck


class GraveLayer(CardLayer):
    def __init__(self, game_state):
        super(GraveLayer, self).__init__(game_state)
        #self.card_list = player.grave