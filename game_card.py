import constants as c
import pygame
import pygame.sprite as sprite


class CardBackground(sprite.Sprite):
    def __init__(self):
        super(CardBackground, self).__init__()

        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)


class CardImage(sprite.Sprite):
    def __init__(self, card_id):
        super(CardImage, self).__init__()

        self.image = pygame.image.load('resources/{:0>3d}.png'.format(card_id))


class CardSprite(sprite.Sprite):
    def __init__(self, card_obj):
        super(CardSprite, self).__init__()

        self.card = card_obj
        self.image = pygame.Surface([c.CARD_WIDTH, c.CARD_HEIGHT])
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()

        name_font = pygame.font.SysFont("comicsansms", 14)
        stat_font = pygame.font.SysFont("comicsansms", 12)

        self.card_name = name_font.render(self.card.name, True, c.BLACK, c.GRAY)
        self.card_image = CardImage(self.card.id).image
        self.card_atk = stat_font.render(str(self.card.attack), True, c.BLACK, c.GRAY)
        self.card_def = stat_font.render(str(self.card.defense), True, c.BLACK, c.GRAY)

        self.image.blit(self.card_name, (c.NAME_LEFT, c.NAME_TOP))
        self.image.blit(self.card_image, (c.IMG_LEFT, c.IMG_TOP))
        self.image.blit(self.card_atk, (c.STAT_LEFT, c.STAT_TOP))
        self.image.blit(self.card_def, (c.STAT_LEFT, c.STAT_TOP + 20))


class GameButton(sprite.Sprite):
    def __init__(self, text, x, y):
        super(GameButton, self).__init__()
        self.image = pygame.Surface((c.BUTTON_W, c.BUTTON_H))
        self.image.fill(c.BUTTON_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._font = pygame.font.SysFont("comicsansms", 12)
        self.text = text

        self.button_text = self._font.render(self.text, True, c.BLACK)
        self.image.blit(self.button_text, (0, 0))


class Cursor(sprite.Sprite):
    def __init__(self, x, y):
        super(Cursor, self).__init__()
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y