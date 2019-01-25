class Action:
    def __init__(self, name):
        self.name = name

    def action(self):
        pass

    def validate(self):
        pass


class DrawAction(Action):
    def __init__(self, player):
        super(DrawAction, self).__init__('draw')
        self.player = player

    def action(self):
        self.player.hand.append(self.player.deck.draw_card())
        self.player.draw()

    def validate(self):
        if self.player.check_draw():
            return True


class SummonAction(Action):
    def __init__(self, player_card, player):
        super(SummonAction, self).__init__('summon')
        self.card = player_card
        self.player = player

    def action(self):
        self.player.summon(self.card)

    def validate(self):
        if self.player.check_summon():
            return True


class EndAction(Action):
    def __init__(self):
        super(EndAction, self).__init__('end')

    def action(self):
        pass
