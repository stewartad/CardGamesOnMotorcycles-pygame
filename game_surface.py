import pygame
import constants as c
import game_card as g_card
import game_state as g_state


class GameSurface(pygame.sprite.RenderClear):
    def __init__(self, game_state):
        super(GameSurface, self).__init__()

        self.surface = pygame.Surface([c.WIN_W, c.WIN_H])
        self.game = game_state
        self.player = self.game.player
        self.hand_group = pygame.sprite.Group()

        self.update()

    def clear_hand(self, surface):
        self.player.hand.clear(self.surface, pygame.Surface([c.WIN_W, c.WIN_H]))

    def update(self, *args):

        for card in self.game.player.hand:
            self.hand.add(g_card.CardSprite(card))
        self.hand.draw(self.surface)
