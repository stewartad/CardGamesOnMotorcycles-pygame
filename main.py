# import the pygame module, so you can use it
import pygame
from pygame.locals import *
import cevent
import constants as c
import game_surface
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
        self.hand_layer = pygame.sprite.Group()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((c.WIN_W, c.WIN_H), pygame.HWSURFACE)
        self._running = True
        self.background = pygame.Surface((c.WIN_W, c.WIN_H))
        self.background.fill(c.BG_BLUE)
        self._image_surf = pygame.image.load("logo32x32.png").convert()
        self.new_game.start_game()

    def on_loop(self):
        i = 0
        self.hand_layer.empty()

        for card in self.new_game.player.hand:
            card_sprite = game_card.CardSprite(card)
            card_sprite.rect.x = i * card_sprite.rect.width + (i + 1) * c.CARD_DIST
            card_sprite.rect.y = c.CARD_DIST
            self.hand_layer.add(card_sprite)
            i = i + 1

        self.hand_layer.update()

    def on_render(self):
        self._display_surf.blit(self.background, (0, 0))
        self.hand_layer.draw(self.background)
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
            print('draw card')
            self.new_game.draw_card(1)
        elif event.key == pygame.K_ESCAPE:
            pygame.quit()

    def on_lbutton_down(self, event):
        print('draw card')
        self.new_game.draw_card(1)






if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
