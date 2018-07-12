# import the pygame module, so you can use it
import pygame
import copy
from pygame.locals import *
import cevent
import constants as c
import game_state
import game_ui
import actions


class App(cevent.CEvent):
    def __init__(self):
        super(App, self).__init__()
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.background = None

        self.clock = pygame.time.Clock()
        self.new_game = game_state.GameState()

        self.draw_b = None
        self.phase_b = None
        self.reset_b = None
        self.exit_b = None

        self.hand_layer = pygame.sprite.Group()
        self.field_layer = pygame.sprite.Group()

        self.game_font = None

        self.buttons = pygame.sprite.Group()
        self.card_preview = pygame.sprite.GroupSingle()

    def refresh_hand(self):
        i = 0
        player_hand = self.new_game.player.hand
        if len(self.hand_layer) > len(player_hand):
            for sprite in self.hand_layer.sprites():
                if not self.new_game.player.check_hand(sprite.card):
                    self.clear_layer(self.hand_layer, sprite.rect)
        self.hand_layer.empty()
        for card in player_hand:
            card_sprite = game_ui.CardSpriteSmall(card)
            card_sprite.rect.x = i * card_sprite.rect.width + (i + 1) * c.CARD_GAP
            card_sprite.rect.y = c.CARD_GAP
            self.hand_layer.add(card_sprite)
            i = i + 1

    def refresh_field(self):
        i = 0
        if len(self.field_layer) > len(self.new_game.player.field):
            for sprite in self.field_layer.sprites():
                if not self.new_game.player.check_field(sprite.card):
                    self.clear_layer(self.field_layer, sprite.rect)
        self.field_layer.empty()
        for card in self.new_game.player.field:
            card_sprite = game_ui.CardSprite(card)
            card_sprite.rect.x = i * card_sprite.rect.width + (i + 1) * c.CARD_GAP
            card_sprite.rect.y = 250
            self.field_layer.add(card_sprite)
            i = i + 1

    def clear_callback(self, surf, rect):
        surf.fill(c.BG_BLUE, rect)
        return surf

    def clear_layer(self, layer, rect):
        layer.clear(self.background, self.clear_callback(self.background, rect))

    def create_card_preview(self, card_sprite):
        curr_card_sprite = self.card_preview.sprite
        new_card_sprite = card_sprite.swap_size()
        if not curr_card_sprite or curr_card_sprite.name != new_card_sprite.name:
            self.card_preview.add(game_ui.CardPreview(new_card_sprite, c.VIEW_LEFT, c.VIEW_TOP))

    def check_game_button(self, button):
        if button.text.lower() == 'draw':
            self.new_game.receive_action(actions.DrawAction(self.new_game.player))
        elif button.text.lower() == 'next phase':
            self.new_game.pass_phase()
        elif button.text.lower() == 'reset':
            self.new_game.reset_game()
            self.card_preview.empty()
            #self.clear_layer(self.hand_layer, self.background.get_rect())
            #self.clear_layer(self.field_layer, self.background.get_rect())
            self.refresh_hand()
            self.refresh_field()
        elif button.text.lower() == 'exit':
            exit()

    def send_action(self, action):
        self.new_game.receive_action(action)

    def on_init(self):
        pygame.init()
        self.game_font = pygame.font.SysFont(c.F_TIMES, 18)
        self._display_surf = pygame.display.set_mode((c.WIN_W, c.WIN_H), pygame.HWSURFACE)
        self._running = True
        self.background = pygame.Surface((c.WIN_W, c.WIN_H))
        self.background.fill(c.BG_BLUE)
        self._image_surf = pygame.image.load("logo32x32.png").convert()

        self.new_game.start_game()

        self.draw_b = game_ui.GameButton('Draw', 100, 800)
        self.phase_b = game_ui.GameButton('Next Phase', 250, 800)
        self.reset_b = game_ui.GameButton('Reset', 400, 800)
        self.exit_b = game_ui.GameButton('Exit', 550, 800)
        self.buttons.add(self.draw_b, self.phase_b, self.reset_b, self.exit_b)

    def on_loop(self):
        self.new_game.update()
        self.refresh_hand()
        self.refresh_field()
        self.hand_layer.update()
        self.field_layer.update()
        self.buttons.update()

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        gs = 'Hand: {}    Deck: {}    {}'.format(len(self.new_game.player.hand), len(self.new_game.player.deck),
                                                 self.new_game.curr_phase.name)
        self._display_surf.blit(self.game_font.render(gs, True, c.BLACK), (c.CENTER_X, 800))
        self.hand_layer.draw(self.background)
        self.field_layer.draw(self.background)
        self.buttons.draw(self.background)
        self.card_preview.draw(self.background)
        pygame.display.flip()

    def on_exit(self):
        self._running = False

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()

    def on_key_down(self, event):
        if event.key == pygame.K_SPACE:
            pass
        elif event.key == pygame.K_ESCAPE:
            exit()

    def on_mouse_move(self, event):
        x = event.pos[0]
        y = event.pos[1]
        cursor = game_ui.Cursor(x, y)
        hover_card = pygame.sprite.spritecollide(cursor, self.hand_layer, False)
        if hover_card:
            self.create_card_preview(hover_card[0])

    def on_lbutton_down(self, event):

        # Creates a 1 x 1 sprite on clicked pixel and checks collision with ui elements

        cursor = game_ui.Cursor(event.pos[0], event.pos[1])
        clicked_button = pygame.sprite.spritecollide(cursor, self.buttons, False)
        clicked_card = pygame.sprite.spritecollide(cursor, self.hand_layer, False)
        if clicked_button:
            self.check_game_button(clicked_button[0])
        elif clicked_card:
            self.send_action(actions.SummonAction(clicked_card[0].card, self.new_game.player))


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
