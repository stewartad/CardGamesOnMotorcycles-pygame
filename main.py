# import the pygame module, so you can use it
import pygame
import copy
from pygame.locals import *
import cevent
import constants as c
import game_state
import game_card


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
        self.reset_b = None
        self.exit_b = None

        self.hand_layer = pygame.sprite.Group()

        self.game_font = None

        self.buttons = pygame.sprite.Group()
        self.card_preview = pygame.sprite.Group()

    def clear_hand(self):
        i = 0
        self.hand_layer.empty()
        for card in self.new_game.player.hand:
            card_sprite = game_card.CardSprite(card)
            card_sprite.rect.x = i * card_sprite.rect.width + (i + 1) * c.CARD_DIST
            card_sprite.rect.y = c.CARD_DIST
            self.hand_layer.add(card_sprite)
            i = i + 1

    def clear_callback(self, surf, rect):
        surf.fill(c.BG_BLUE, rect)
        return surf

    def create_card_preview(self, card_sprite):
        self.card_preview.empty()
        new_card = game_state.Card(card_sprite.card.get_info())

        new_card_sprite = game_card.CardSprite(new_card)
        new_card_sprite.rect.x = 1305
        new_card_sprite.rect.y = 485

        new_card_type_label = game_card.GameLabel('Type: {}'.format(new_card.card_type), 1305, 752, 18)
        new_card_attr_label = game_card.GameLabel('Attribute: {}'.format(new_card.attribute), 1305, 802, 18)
        self.card_preview.add(new_card_sprite, new_card_type_label, new_card_attr_label)

    def on_init(self):
        pygame.init()
        self.game_font = pygame.font.SysFont(c.F_TIMES, 18)
        self._display_surf = pygame.display.set_mode((c.WIN_W, c.WIN_H), pygame.HWSURFACE)
        self._running = True
        self.background = pygame.Surface((c.WIN_W, c.WIN_H))
        self.background.fill(c.BG_BLUE)
        self._image_surf = pygame.image.load("logo32x32.png").convert()

        self.new_game.start_game()

        self.draw_b = game_card.GameButton('Draw', 100, 800)
        self.reset_b = game_card.GameButton('Reset', 250, 800)
        self.exit_b = game_card.GameButton('Exit', 400, 800)
        self.buttons.add(self.draw_b, self.reset_b, self.exit_b)

    def on_loop(self):
        self.clear_hand()
        self.hand_layer.update()
        self.buttons.update()

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        gs = 'Hand: {}    Deck: {}'.format(len(self.new_game.player.hand), len(self.new_game.player.deck))
        self._display_surf.blit(self.game_font.render(gs,True, c.BLACK), (c.CENTER_X, 800))
        self.hand_layer.draw(self.background)
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
        cursor = game_card.Cursor(x, y)
        hover_card = pygame.sprite.spritecollide(cursor, self.hand_layer, False)
        # This should be moved to a function
        if hover_card:
            self.card_preview.empty()
            self.create_card_preview(hover_card[0])


    def on_lbutton_down(self, event):
        print(event.pos)
        x = event.pos[0]
        y = event.pos[1]
        cursor = game_card.Cursor(x, y)
        clicked_button = pygame.sprite.spritecollide(cursor, self.buttons, False)
        clicked_card = pygame.sprite.spritecollide(cursor, self.hand_layer, False)
        if clicked_button:
            if clicked_button[0].text.lower() == 'draw':
                self.new_game.draw_card(1)
            elif clicked_button[0].text.lower() == 'reset':
                self.new_game.reset_game()
                self.card_preview.empty()
                self.hand_layer.clear(self.background, self.clear_callback(self.background, self.background.get_rect()))
                self.clear_hand()
            elif clicked_button[0].text.lower() == 'exit':
                exit()
        elif clicked_card:
            print(str(clicked_card[0].card))






if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
