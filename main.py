# import the pygame module, so you can use it
import pygame
import copy
from pygame.locals import *
import cevent
import constants as c
import game_state
import game_ui


class App(cevent.CEvent):
    def __init__(self):
        super(App, self).__init__()
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.background = None
        self.game_ui = None

        self.clock = pygame.time.Clock()
        self.current_game = game_state.GameState()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((c.WIN_W, c.WIN_H), pygame.HWSURFACE)
        self._running = True
        self.background = pygame.Surface((c.WIN_W, c.WIN_H))
        self.background.fill(c.BG_BLUE)
        self._image_surf = pygame.image.load("logo32x32.png").convert()

        self.game_ui = game_ui.GameUI(self.current_game)

    def on_loop(self):
        self.current_game.update()
        self.game_ui.update()

    def on_render(self):
        self.game_ui.draw(self.background)
        self._display_surf.blit(self.background, (0, 0))

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
        self.game_ui.on_hover(event.pos[0], event.pos[1])

    def on_lbutton_down(self, event):
        self.game_ui.on_click(event.pos[0], event.pos[1])


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
