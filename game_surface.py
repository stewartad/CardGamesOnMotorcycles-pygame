import pygame
import constants as c
import game_card as g_card
import game_state as g_state


class GameSurface(pygame.sprite.RenderClear):
    def __init__(self):
        super(GameSurface, self).__init__()

        self.surface = pygame.Surface([c.WIN_W, c.WIN_H])
        self.game = g_state.GameState()
        self.hand = pygame.sprite.Group()

        self.update()

    def update(self, *args):
        self.hand.clear(self.surface, pygame.Surface([c.WIN_W, c.WIN_H]))
        for card in self.game.player.hand:
            self.hand.add(g_card.CardSprite(card))
        self.hand.draw(self.surface)
