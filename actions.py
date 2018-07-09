import constants as c


class Action:
    def __init__(self, name):
        self.name = name
        self.valid = False

    def action(self):
        pass

    def validate(self):
        pass


class DrawAction(Action):
    def __init__(self, player, n):
        super(DrawAction, self).__init__('draw')
        self.player = player
        self.n = n

    def action(self):
        for i in range(self.n):
            self.player.hand.append(self.player.deck.draw_card())

    def validate(self):
        if len(self.player.hand) <= c.HAND_MAX - self.n and len(self.player.deck) != 0:
            self.valid = True
        return self.valid


class SummonAction(Action):
    def __init__(self, player_card, player_field):
        super(SummonAction, self).__init__('summon')
        self.card = player_card
        self.field = player_field

    def action(self):
        self.field.append(self.card)