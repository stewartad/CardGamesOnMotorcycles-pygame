import actions
from card_view import HandView, FieldView
from ui_elements import *
from pygame.locals import *


# Super class for UI state machine
# NOTE all state rects must be the same size so that sprite collision works
# The cursor sprite is created with respect to the window size
# Any elements must be sprites positioned relative to the parent rect
class State:
    def __init__(self, game_state):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

        self.game_state = game_state

        self.active_sprites = sprite.Group()
        self.buttons = sprite.Group()
        self.preview = sprite.GroupSingle()

        self.reset = False
        self.quit = False

    def draw(self, surface_obj):
        pass

    def update(self):
        pass

    def startup(self):
        pass

    def cleanup(self):
        pass

    def check_button(self, button):
        pass

    def get_event(self, event):
        if event.type == KEYUP:
            pass
        elif event.type == KEYDOWN:
            self.on_key_down(event.key)
        elif event.type == MOUSEMOTION:
            self.on_hover(event.pos[0], event.pos[1])
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                pass
            elif event.button == 2:
                pass
            elif event.button == 3:
                pass
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_click(event.pos[0], event.pos[1])
            elif event.button == 2:
                pass
            elif event.button == 3:
                pass

    def on_key_down(self, key):
        pass

    def on_click(self, x, y):
        cursor = Cursor(x, y)
        clicked_button = pygame.sprite.spritecollide(cursor, self.buttons, False)
        if clicked_button:
            self.check_button(clicked_button[0])

    def on_hover(self, x, y):
        cursor = Cursor(x, y)
        hover_card = pygame.sprite.spritecollide(cursor, self.active_sprites, False)
        if hover_card:
            self.preview.add(CardSprite(hover_card[0].card, c.VIEW_LEFT, c.VIEW_TOP))


# Class for the "pause" menu
class Menu(State):
    def __init__(self, game_state):
        super(Menu, self).__init__(game_state)
        self.next = 'board'

        self.rect = pygame.Rect(0, 0, c.WIN_W, c.WIN_H)

        self.background = Block(c.GRAY, c.CENTER_X - 75, c.CENTER_Y - 75, 150, 150)
        reset_b = Button('Reset', c.CENTER_X - 50, c.CENTER_Y - 50)
        exit_b = Button('Exit', c.CENTER_X - 50, c.CENTER_Y + 10)
        self.buttons.add(reset_b, exit_b)

    def check_button(self, button):
        if button.text.lower() == 'reset':
            self.game_state.reset_game()
            self.done = True
        elif button.text.lower() == 'exit':
            self.quit = True
            print("Exiting")

    def on_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.done = True

    def draw(self, surface_obj):
        self.background.draw(surface_obj)
        self.buttons.draw(surface_obj)

    def update(self):
        self.buttons.update()


# Main game UI
class GameUI(State):
    def __init__(self, game_state):
        super(GameUI, self).__init__(game_state)
        self.font = pygame.font.SysFont(c.F_TIMES, 18)
        self.image = pygame.Surface((c.WIN_W, c.WIN_H))
        self.rect = pygame.Rect(0, 0, c.WIN_W, c.WIN_H)

        self.player = game_state.player

        self.player_hand = HandView(20, 20, self.player)
        self.player_field = FieldView(20, 250, self.player)

        draw_b = Button('Draw', 100, c.WIN_H - c.BUTTON_H - 50)
        phase_b = Button('Next Phase', 250, c.WIN_H - c.BUTTON_H - 50)
        #reset_b = Button('Reset', 400, 800)
        #exit_b = Button('Exit', 550, 800)
        deck_b = Button('View Deck', 500, c.WIN_H - c.BUTTON_H - 50)
        #disc_b = Button('View Discard', 850, 800)
        self.buttons.add(draw_b, phase_b, deck_b)

    def start_game(self):
        self.game_state.start_game()

    def check_button(self, button):
        if button.text.lower() == 'draw':
            self.game_state.receive_action(actions.DrawAction(self.player))
        elif button.text.lower() == 'next phase':
            self.game_state.pass_phase()
        elif button.text.lower() == 'reset':
            self.game_state.reset_game()
            self.preview.empty()
        elif button.text.lower() == 'exit':
            exit()
        elif button.text.lower() == 'view deck':
            self.next = 'deck'
            self.done = True
        elif button.text.lower() == 'view discard':
            self.next = 'discard'
            self.done = True

    def draw(self, surface_obj):
        surface_obj.blit(self.image, self.rect)
        self.preview.draw(surface_obj)
        self.player_hand.draw(surface_obj)
        self.player_field.draw(surface_obj)
        self.buttons.draw(surface_obj)

    def update(self):
        self.image.fill(c.BG_BLUE)
        self.image.blit(
            self.font.render('Turn: {}  {}'.format(self.game_state.turn_count, self.game_state.curr_phase.name),
                             True,
                             c.BLACK),
            (c.LABEL_LEFT, c.LABEL_TOP))
        self.buttons.update()
        self.preview.update()

        self.player_hand.update()
        self.player_field.update()
        self.active_sprites.empty()
        self.active_sprites.add(self.player_hand.sprites, self.player_field.sprites_group)

    def on_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.next = 'pause'
            self.done = True

    def on_click(self, x, y):
        cursor = Cursor(x, y)
        clicked_card = pygame.sprite.spritecollide(cursor, self.player_hand.sprites_group, False)
        if clicked_card:
            self.game_state.receive_action(actions.SummonAction(clicked_card[0].card, self.game_state.player, self.player_field.get_location(x, y)))
        else:
            super(GameUI, self).on_click(x, y)

    def on_hover(self, x, y):
        cursor = Cursor(x, y)
        hover_card = pygame.sprite.spritecollide(cursor, self.active_sprites, False)
        if hover_card:
            self.preview.add(CardSprite(hover_card[0].card, c.VIEW_LEFT, c.VIEW_TOP))
