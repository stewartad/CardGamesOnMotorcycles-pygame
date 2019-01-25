import constants as c
import random
import parse
import actions


class GameState:
    def __init__(self):
        self.player = Player("Yugi")
        self.phases = [Phase('Draw Phase', 'draw'), Phase('Main Phase', 'summon'), Phase('End Phase', 'end')]
        self.phase_index = 0
        self.curr_phase = self.phases[self.phase_index]
        self.turn_stack = []
        self.turn_count = 0

    def draw_card(self, n):
        if len(self.player.hand) <= c.HAND_MAX - n and len(self.player.deck) != 0:
            for i in range(n):
                self.player.hand.append(self.player.deck.draw_card())

    def reset_game(self):
        self.turn_count = 0
        self.turn_stack.clear()
        self.player.hand.clear()
        self.player.field.clear()
        self.player.deck.reset()
        self.start_game()

    def start_game(self):
        self.player.deck.shuffle()
        self.draw_card(c.HAND_SIZE)
        self.new_turn()

    def receive_action(self, action):
        # Method to add action to the turn stack to be executed later
        # Action validation will be extended to implement player priority, probably by passing game state
        if action.name in self.curr_phase.allowed_actions and action.validate():
            self.turn_stack.append(action)

    def pass_phase(self):
        # Increment phase count
        self.phase_index = self.phase_index + 1
        if self.curr_phase.name == 'End Phase':
            self.new_turn()

    def new_turn(self):
        # reset phase counter and once per turn actions
        self.turn_count = self.turn_count + 1
        self.phase_index = 0
        self.player.can_summon = True
        self.player.can_draw = True

    def update(self):
        self.curr_phase = self.phases[self.phase_index]
        while self.turn_stack:
            action = self.turn_stack.pop(0)
            action.action()


class Phase:
    # Keeps track of action types that are allowed in each phase of the turn
    def __init__(self, name, *args):
        self.name = name
        self.allowed_actions = list(args)


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.field = []
        self.deck = Deck(c.DEFAULT_DECK)
        self.can_draw = True
        self.can_summon = True

    def check_draw(self):
        if len(self.hand) <= c.HAND_MAX - 1 and len(self.deck) != 0 and self.can_draw:
            self.can_draw = True
        else:
            self.can_draw = False
        return self.can_draw

    def draw(self):
        if self.can_draw:
            self.can_draw = False

    def revoke_summon(self):
        self.can_summon = False

    def check_summon(self):
        if len(self.field) < c.FIELD_MAX and self.can_summon:
            return True
        else:
            self.revoke_summon()
            return False

    def summon(self, card):
        if self.can_summon:
            self.can_summon = False
            self.hand.remove(self.check_hand(card))
            self.field.append(card)

    def check_hand(self, card):
        return next((x for x in self.hand if x.id == card.id), None)

    def check_field(self, card):
        return next((x for x in self.field if x.id == card.id), None)


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