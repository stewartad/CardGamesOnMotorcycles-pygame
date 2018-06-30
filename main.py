# import the pygame module, so you can use it
import pygame
import constants as c
import game_surface
import game_state
import game_card


# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")

    clock = pygame.time.Clock()

    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((c.WIN_W, c.WIN_H))

    # define a variable to control the main loop
    running = True

    background = pygame.Surface((c.WIN_W, c.WIN_H))
    background = background.convert()
    background.fill(c.BG_BLUE)

    new_game = game_state.GameState()
    new_game.start_game()

    hand_layer = pygame.sprite.Group()

    hand = new_game.player.hand
    for card in new_game.player.hand:
        hand_layer.add(game_card.CardSprite(card))

    i = 0
    for card in hand_layer:
        card.rect.x =  i * card.rect.width + (i + 1) * c.CARD_DIST
        card.rect.y = c.CARD_DIST
        i = i + 1
    hand_layer.draw(background)


    # main loop
    while running:


        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()