import constants as c
import random
import parse
import actions


class GameState:
    def __init__(self):
        self.player = Player("Yugi")
        self.phases = [Phase('Draw Phase', 'draw'), Phase('Main Phase', 'summon')]
        self.curr_phase = self.phases[0]
        self.turn_stack = []

    def draw_card(self, n):
        if len(self.player.hand) <= c.HAND_MAX - n and len(self.player.deck) != 0:
            for i in range(n):
                self.player.hand.append(self.player.deck.draw_card())

    def reset_game(self):
        self.player.hand.clear()
        self.player.deck.reset()
        self.start_game()

    def start_game(self):
        self.player.deck.shuffle()
        self.draw_card(c.HAND_SIZE)

    def receive_action(self, action):
        if action.name in self.curr_phase.allowed_actions and action.validate():
            self.turn_stack.append(action)

    def pass_phase(self):
        self.curr_phase = self.curr_phase + 1

    def update(self):
        while self.turn_stack:
            action = self.turn_stack.pop(0)
            action.validate()
            action.action()


class Phase:
    def __init__(self, name, *args):
        self.name = name
        self.allowed_actions = list(args)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.field = []
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
            self.deck.append(Card(parse.get_card_query(cardID)))

    def reset(self):
        self.deck.clear()
        self.populate_deck()

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_card(self):
        return self.deck.pop(0)


class Card:
    def __init__(self, card_info):
        self.id = int(card_info[c.CARD_ID])
        self.name = card_info[c.CARD_NAME]
        self.image = card_info[c.CARD_IMAGE]
        self.card_type = card_info[c.CARD_TYPE]
        self.attribute = card_info[c.ATTRIBUTE]
        self.attack = card_info[c.ATK]
        self.defense = card_info[c.DEF]
        self.EFFECT = card_info[c.EFFECT]

    def __str__(self):
        return self.name

    def get_info(self):
        return [self.id, self.name, self.image, self.card_type, self.attribute, self.attack, self.defense, self.EFFECT]

    def get_game_info(self):
        return {'id': self.id,
                'name': self.name,
                'image': self.image,
                'card type': self.card_type,
                'attribute': self.attribute,
                'attack': str(self.attack),
                'defense': str(self.defense),
                'effect': self.EFFECT}