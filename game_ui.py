import constants as c
import pygame
import pygame.sprite as sprite
import actions


class CardSprite(sprite.Sprite):
    def __init__(self, card_obj, x, y):
        super(CardSprite, self).__init__()
        self.card = card_obj
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.rect = pygame.Rect(x, y, c.CARD_WIDTH, c.CARD_HEIGHT)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.WHITE)
        name_font = pygame.font.SysFont(c.F_TIMES, 14)
        stat_font = pygame.font.SysFont(c.F_TIMES, 12)

        card_name = name_font.render(self.card.name, True, c.BLACK)
        card_image = pygame.image.load('resources/{:0>3d}.png'.format(self.card.id))
        card_image = pygame.transform.scale(card_image, (c.IMG_WIDTH, c.IMG_HEIGHT))
        card_atk = stat_font.render(str(self.card.attack), True, c.BLACK)
        card_def = stat_font.render(str(self.card.defense), True, c.BLACK)

        self.image.blit(card_name, c.NAME_CORNER)
        self.image.blit(card_image, c.IMG_CORNER)
        if self.card.card_type == 'MONSTER':
            self.image.blit(card_atk, c.ATK_CORNER)
            self.image.blit(card_def, c.DEF_CORNER)


class SmallCardSprite(sprite.Sprite):
    def __init__(self, card_obj, x=0, y=0):
        super(SmallCardSprite, self).__init__()
        self.card = card_obj
        self.name = self.card.name
        self.image = pygame.Surface([c.S_CARD_WIDTH, c.S_CARD_HEIGHT])
        self.rect = pygame.Rect(x, y, c.S_CARD_WIDTH, c.S_CARD_HEIGHT)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.WHITE)
        name_font = pygame.font.SysFont(c.F_TIMES, 12)

        card_name = name_font.render(self.card.name, True, c.BLACK)
        card_image = pygame.image.load('resources/{:0>3d}.png'.format(self.card.id))
        card_image = pygame.transform.scale(card_image, (c.S_IMG_WIDTH, c.S_IMG_HEIGHT))

        self.image.blit(card_name, c.S_NAME_CORNER)
        self.image.blit(card_image, c.S_IMG_CORNER)


class Button(sprite.Sprite):
    def __init__(self, text, x, y):
        super(Button, self).__init__()
        self.text = text
        self.image = pygame.Surface([c.BUTTON_W, c.BUTTON_H])
        self.rect = pygame.Rect(x, y, c.BUTTON_W, c.BUTTON_H)

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)

    def update(self):
        self.image.fill(c.BUTTON_COLOR)
        name_font = pygame.font.SysFont(c.F_TIMES, 14)
        button_text = name_font.render(self.text, True, c.BLACK)
        size = name_font.size(self.text)
        center = ((self.rect.width - size[0]) / 2, (self.rect.height - size[1]) /2)

        self.image.blit(button_text, center)


class Cursor(sprite.Sprite):
    def __init__(self, x, y):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((10, 10))
        self.rect = pygame.Rect(x, y, 10, 10)


class PlayerHand:
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


class PlayerField:
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


class GameUI:
    def __init__(self, game_state):
        self.font = pygame.font.SysFont(c.F_TIMES, 18)
        self.image = pygame.Surface((c.WIN_W, c.WIN_H))
        self.rect = (0, 0, c.WIN_W, c.WIN_H)

        self.game_state = game_state
        self.player1 = game_state.player

        self.buttons = sprite.RenderClear()
        self.preview = sprite.GroupSingle()

        draw_b = Button('Draw', 100, 800)
        phase_b = Button('Next Phase', 250, 800)
        reset_b = Button('Reset', 400, 800)
        exit_b = Button('Exit', 550, 800)
        self.buttons.add(draw_b, phase_b, reset_b, exit_b)

        self.player1_hand = PlayerHand(20, 20, self.player1)
        self.player1_field = PlayerField(20, 250, self.player1)
        self.active_sprites = sprite.Group()

        self.game_state.start_game()

    def check_button(self, button):
        if button.text.lower() == 'draw':
            self.game_state.receive_action(actions.DrawAction(self.player1))
        elif button.text.lower() == 'next phase':
            self.game_state.pass_phase()
        elif button.text.lower() == 'reset':
            self.game_state.reset_game()
            self.preview.empty()
        elif button.text.lower() == 'exit':
            exit()

    def on_hover(self, x, y):
        cursor = Cursor(x, y)
        hover_card = pygame.sprite.spritecollide(cursor, self.active_sprites, False)
        if hover_card:
            self.preview.add(CardSprite(hover_card[0].card, c.VIEW_LEFT, c.VIEW_TOP))

    def on_click(self, x, y):
        cursor = Cursor(x, y)
        clicked_button = pygame.sprite.spritecollide(cursor, self.buttons, False)
        clicked_card = pygame.sprite.spritecollide(cursor, self.player1_hand.sprites_group, False)
        if clicked_button:
            self.check_button(clicked_button[0])
        elif clicked_card:
            self.game_state.receive_action(actions.SummonAction(clicked_card[0].card, self.game_state.player))

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)
        self.preview.draw(surface_obj)
        self.player1_hand.draw(surface_obj)
        self.player1_field.draw(surface_obj)
        self.buttons.draw(surface_obj)

    def update(self):
        self.image.fill(c.BG_BLUE)
        self.image.blit(
            self.font.render('Hand: {}    Deck: {}    Turn: {}    {}'.format(len(self.game_state.player.hand),
                                                                             len(self.game_state.player.deck),
                                                                             self.game_state.turn_count,
                                                                             self.game_state.curr_phase.name),
                             True,
                             c.BLACK),
            (c.CENTER_X, 800))
        self.buttons.update()
        self.preview.update()
        self.player1_hand.update()
        self.player1_field.update()
        self.active_sprites.empty()
        self.active_sprites.add(self.player1_hand.sprites, self.player1_field.sprites)
