# import the pygame module, so you can use it
import pygame

import card_layer
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

        self.state_dict = None
        self.state_name = None
        self.state = None

        self.clock = pygame.time.Clock()
        self.current_game = game_state.GameState()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((c.WIN_W, c.WIN_H), pygame.HWSURFACE)
        self._running = True
        self.background = pygame.Surface((c.WIN_W, c.WIN_H))
        self.background.fill(c.BG_BLUE)
        self._image_surf = pygame.image.load("logo32x32.png").convert()

        # Vars to turn this class into a state machine controller
        # This is atrocious and will be rewritten
        # The main game ui will act as the controller for ui states eventually
        # currently the game ui is a state and its time to see if it works

        self.state_dict = {'board': game_ui.GameUI(self.current_game),
                           'deck': card_layer.DeckLayer(self.current_game),
                           'pause': game_ui.Menu(self.current_game)}
        self.state_name = 'board'
        self.state = self.state_dict[self.state_name]

        # self.game_ui = game_ui.GameUI(self.current_game)
        self.game_ui = self.state_dict['board']
        self.game_ui.start_game()

    def flip_state(self):
        self.state.done = False
        previous = self.state_name
        self.state_name = self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def on_loop(self):
        self.current_game.update()
        self.state.update()

        if self.state.quit:
            self.on_exit()
        elif self.state.done:
            self.flip_state()
        self.state.update()

    def on_render(self):
        self.state.draw(self.background)
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
                # self.on_event(event)
                if event.type == pygame.QUIT:
                    self._running = False
                self.state.get_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(60)
        self.on_cleanup()

    # def on_key_down(self, event):
    #     if event.key == pygame.K_SPACE:
    #         pass
    #     elif event.key == pygame.K_ESCAPE:
    #         exit()
    #
    # def on_mouse_move(self, event):
    #     self.game_ui.on_hover(event.pos[0], event.pos[1])
    #
    # def on_lbutton_down(self, event):
    #     self.game_ui.on_click(event.pos[0], event.pos[1])


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
