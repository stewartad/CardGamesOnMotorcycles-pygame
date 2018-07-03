import constants as c
import random
import game_card as card
import parse


class GameState:
    def __init__(self):
        self.player = Player("Yugi")

    def draw_card(self, n):
        if len(self.player.hand) <= c.HAND_MAX - n:
            for i in range(n):
                self.player.hand.append(self.player.deck.draw_card())

    def reset_game(self):
        self.player.hand.clear()
        self.player.deck.reset()
        self.start_game()

    def start_game(self):
        self.player.deck.shuffle()
        self.draw_card(c.HAND_SIZE)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.deck = Deck(c.DEFAULT_DECK)


class Deck:
    def __init__(self, deck_list):
        self.deckList = deck_list
        self.deck = []
        self.populate_deck()

    def __len__(self):
        return len(self.deck)

    def __str__(self):
        return str(self.deck)

    def populate_deck(self):
        for cardID in self.deckList:
            self.deck.append(card.Card(parse.get_card_query(cardID)))

    def reset(self):
        self.deck.clear()
        self.populate_deck()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop(0)
